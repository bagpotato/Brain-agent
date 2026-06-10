#!/usr/bin/env python3
"""
brain_agent.py — Local agent for adding notes to an Obsidian vault.
Uses Ollama as a local AI backend.

Usage:
  python brain_agent.py "topic or note prompt"
  python brain_agent.py --interactive
"""

import argparse
import datetime
import json
import os
import re
import sys
import urllib.request
import urllib.error

# ─── CONFIGURATION ────────────────────────────────────────────────────────────

VAULT_PATH = os.path.expanduser("~/Vault")   # <- change this to your vault path
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL      = "qwen2.5:7b"                    # recommended model

FOLDERS = {
    "areas":     "Areas",
    "project":   "Projects",
    "resource":  "Resources",
    "goal":      "Goals",
    "note":      "Notes",          # generic folder
}

# ─── SYSTEM PROMPT ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are a knowledge management agent for an Obsidian vault.
Your job is to generate perfectly formatted Markdown notes for the user
to save in their second brain.

MANDATORY RULES:
1. Respond ONLY with the Markdown content of the note. No explanations, no extra
   code blocks, no text before or after.
2. Always include a YAML frontmatter block at the beginning with: tags, date, type.
3. Use [[internal links]] to connect to other vault notes when relevant.
4. The first line after the frontmatter is always an H1 heading with an emoji.
5. Notes must be concrete, useful, and actionable — not generic.
6. Include relevant sections depending on the note type (see below).

NOTE TYPES AND THEIR SECTIONS:

type: concept
  - What it is / Definition
  - Why it matters
  - How it works (technical)
  - Commands / practical examples (if applicable)
  - Related links [[...]]

type: project
  - Description
  - Goal
  - Stack / Technologies
  - To-do (checkboxes)
  - Related links [[...]]

type: resource
  - What it is
  - Why it is worth it
  - URL / reference
  - Level (beginner / intermediate / advanced)
  - Related links [[...]]

type: goal
  - The goal
  - Why
  - Concrete steps (checkboxes)
  - Deadline or estimated time
  - Related links [[...]]

type: note
  - Free but structured content
  - Related links [[...]]
"""

# ─── FUNCTIONS ────────────────────────────────────────────────────────────────

def call_ollama(prompt: str) -> str:
    """Calls the Ollama API and returns the generated text."""
    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "system": SYSTEM_PROMPT,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.9,
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "").strip()
    except urllib.error.URLError as e:
        print(f"\n❌ Error connecting to Ollama: {e}")
        print("   Make sure Ollama is running: ollama serve")
        sys.exit(1)


def detect_folder(content: str) -> str:
    """Detects the target folder based on the frontmatter or content."""
    match = re.search(r"type:\s*(\w+)", content.lower())
    if match:
        note_type = match.group(1)
        return FOLDERS.get(note_type, "Notes")
    return "Notes"


def extract_title(content: str) -> str:
    """Extracts the title from the note's H1 heading."""
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        # Strip characters that are invalid in file names
        title = re.sub(r'[<>:"/\\|?*]', '', title)
        title = title.strip()
        return title
    return f"note_{datetime.date.today()}"


def save_note(content: str, force_folder: str = None) -> str:
    """Saves the note to the vault and returns the path."""
    folder = force_folder or detect_folder(content)
    title  = extract_title(content)

    directory = os.path.join(VAULT_PATH, folder)
    os.makedirs(directory, exist_ok=True)

    filename = f"{title}.md"
    path = os.path.join(directory, filename)

    # Avoid overwriting
    if os.path.exists(path):
        timestamp = datetime.datetime.now().strftime("%H%M%S")
        filename = f"{title}_{timestamp}.md"
        path = os.path.join(directory, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return path


def generate_note(topic: str) -> None:
    """Full process: generates and saves a note."""
    print(f"\n🧠 Generating note about: {topic}")
    print(f"   Model: {MODEL} | Vault: {VAULT_PATH}\n")

    prompt = f"""Create a complete and useful Obsidian note about the following topic:

{topic}

Remember: respond ONLY with the Markdown of the note, starting with the YAML frontmatter."""

    print("⏳ Thinking...", end="", flush=True)
    content = call_ollama(prompt)
    print(" done.\n")

    if not content:
        print("❌ The AI returned no content. Please try again.")
        return

    path = save_note(content)
    print(f"✅ Note saved at: {path}")
    print("\n─── Preview ──────────────────────────────────────────────")
    # Show the first 20 lines
    lines = content.split("\n")
    print("\n".join(lines[:20]))
    if len(lines) > 20:
        print(f"   ... ({len(lines) - 20} more lines)")
    print("──────────────────────────────────────────────────────────\n")


def interactive_mode() -> None:
    """Interactive loop to generate multiple notes."""
    print("\n🧠 Brain Agent — Interactive mode")
    print(f"   Vault: {VAULT_PATH}")
    print(f"   Model: {MODEL}")
    print("   Type 'exit' to quit.\n")

    while True:
        try:
            topic = input("📝 Note topic: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye.")
            break

        if topic.lower() in ("exit", "quit", "q"):
            print("👋 Goodbye.")
            break

        if not topic:
            continue

        generate_note(topic)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    global VAULT_PATH, MODEL
    parser = argparse.ArgumentParser(
        description="Local AI agent for adding notes to an Obsidian vault"
    )
    parser.add_argument(
        "topic",
        nargs="?",
        help="Topic to generate a note about"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Interactive mode (generate multiple notes)"
    )
    parser.add_argument(
        "--vault",
        default=VAULT_PATH,
        help=f"Path to the Obsidian vault (default: {VAULT_PATH})"
    )
    parser.add_argument(
        "--model",
        default=MODEL,
        help=f"Ollama model to use (default: {MODEL})"
    )

    args = parser.parse_args()

    # Allow overriding config via arguments
    VAULT_PATH = args.vault
    MODEL = args.model

    if not os.path.isdir(VAULT_PATH):
        print(f"⚠️  Vault not found at: {VAULT_PATH}")
        print("   Use --vault /path/to/your/vault")
        sys.exit(1)

    if args.interactive or not args.topic:
        interactive_mode()
    else:
        generate_note(args.topic)


if __name__ == "__main__":
    main()
