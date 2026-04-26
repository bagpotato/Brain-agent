# brain-agent

Local AI agent that generates and saves notes in your [Obsidian](https://obsidian.md) vault using [Ollama](https://ollama.com) as the backend. No cloud, no API keys, no cost.

Designed to work as an **automated second brain**: give it a topic and it generates a well-structured Markdown note with YAML frontmatter, internal `[[links]]` and actionable sections, saving it directly to the correct folder in the vault.

---

## Demo

```
$ brain

Brain Agent — Interactive mode
   Vault: /home/user/Vault
   Model: qwen2.5:7b

Topic: nmap and network reconnaissance

Thinking... done.

Note saved at: /home/user/Vault/Areas/Nmap - Network Scanning.md
```

---

## Requirements

- [Ollama](https://ollama.com) installed and running
- Python 3 (stdlib only, no external dependencies)

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/bagpotato/brain-agent
cd brain-agent
```

### 2. Pull the model

```bash
ollama pull qwen2.5:7b
```

### 3. Set your vault path

Edit `brain_agent.py` line 24:

```python
VAULT_PATH = os.path.expanduser("~/Vault")  # <- your path here
```

---

## Usage

```bash
# Single note
python3 brain_agent.py "nmap and network reconnaissance"

# Interactive mode (multiple notes)
python3 brain_agent.py --interactive

# Specify vault and model manually
python3 brain_agent.py --vault ~/Vault --model qwen2.5:3b "CIDR subnetting"
```

---

## Permanent alias

### NixOS

Add to `/etc/nixos/configuration.nix`:

```nix
programs.zsh.shellAliases = {
  brain = "python3 /path/brain_agent.py --vault /path/vault --interactive";
};
```

```bash
sudo nixos-rebuild switch
```

### Standard Linux (bash/zsh)

```bash
echo 'alias brain="python3 /path/brain_agent.py --vault /path/vault --interactive"' >> ~/.zshrc
source ~/.zshrc
```

---

## Vault structure

The agent detects the note type from the frontmatter and saves it to the correct folder:

```
Vault/
├── Areas/        <- technical concepts, commands, protocols
├── Projects/     <- new projects with to-do and stack
├── Resources/    <- tools, courses, books, websites
├── Goals/        <- goals with roadmap and checkboxes
└── Notes/        <- free-form notes
```

Example generated note (`Areas/Nmap.md`):

```markdown
---
tags: [tool, reconnaissance, network]
date: 2026-04-26
type: concept
---

# Nmap - Network Scanning

<- [[Home]]

## What is it
Nmap is the standard tool for host discovery and port scanning...

## Key commands
| Command | Description |
|---|---|
| `nmap -sn 192.168.1.0/24` | Discover active hosts |
| `nmap -sC -sV -oN scan.txt IP` | Full scan with scripts |

## Related
- [[Networks]]
- [[Cybersecurity]]
```

---

## Models

| Model | RAM | Speed | Quality |
|---|---|---|---|
| `qwen2.5:3b` | 4 GB | fast | good |
| `qwen2.5:7b` | 8 GB | medium | very good (recommended) |
| `qwen2.5:14b` | 12 GB | slow | excellent |

Qwen2.5 follows structured instructions better than Llama or Mistral, which is key for well-formatted Markdown and correct `[[links]]`.

---

## Customization

The AI behavior is controlled from `SYSTEM_PROMPT` in `brain_agent.py`. It defines:

- User profile (interests, professional goal)
- Existing vault notes to link to
- Required format for each note type
- Tone and level of technical detail

`PROMPT_MODEL.md` documents the model in Obsidian format to keep it inside the vault.

---

## Files

| File | Description |
|---|---|
| `brain_agent.py` | Main script |
| `PROMPT_MODEL.md` | System prompt documentation (for the vault) |

---

## License

MIT
