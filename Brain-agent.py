 #!/usr/bin/env python3
"""
brain_agent.py — Agente local para añadir notas al vault de Obsidian
Usa Ollama como backend de IA local.

Uso:
  python brain_agent.py "aprende sobre nmap"
  python brain_agent.py "nuevo proyecto: monitoring con Grafana"
  python brain_agent.py "recurso: libro The Web Application Hacker's Handbook"
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

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────

VAULT_PATH = os.path.expanduser("~/brain")   # ← cambia esto a la ruta de tu vault
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL      = "qwen2.5:7b"                    # modelo recomendado

CARPETAS = {
    "areas":     "Areas",
    "proyecto":  "Proyectos",
    "recurso":   "Recursos",
    "objetivo":  "Objetivos",
    "nota":      "Notas",          # carpeta genérica
}

# ─── SYSTEM PROMPT ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
Eres un agente de gestión de conocimiento para un vault de Obsidian.
Tu trabajo es generar notas Markdown perfectamente formateadas para que el usuario
las guarde en su segundo cerebro.

REGLAS OBLIGATORIAS:
1. Responde SOLO con el contenido Markdown de la nota. Sin explicaciones, sin bloques
   de código extra, sin texto antes o después.
2. Siempre incluye un bloque YAML frontmatter al inicio con: tags, fecha, tipo.
3. Usa [[enlaces internos]] para conectar con otras notas del vault cuando sea relevante.
4. La primera línea después del frontmatter es siempre un heading H1 con emoji.
5. Las notas deben ser concretas, útiles y accionables, no genéricas.
6. Incluye secciones relevantes según el tipo de nota (ver abajo).
7. Adapta el contenido al perfil del usuario: estudiante de SMX en Barcelona,
   interesado en Linux, administración de sistemas, redes y ciberseguridad.
   Su objetivo es trabajar en ciberseguridad.

TIPOS DE NOTA Y SUS SECCIONES:

tipo: concepto
  - Qué es / Definición
  - Por qué importa (en contexto de ciberseguridad/sysadmin)
  - Cómo funciona (técnico)
  - Comandos / ejemplos prácticos (si aplica)
  - Links relacionados [[...]]

tipo: proyecto
  - Descripción
  - Objetivo
  - Stack / Tecnologías
  - To-do (checkboxes)
  - Links relacionados [[...]]

tipo: recurso
  - Qué es
  - Por qué vale la pena
  - URL / referencia
  - Nivel (básico / medio / avanzado)
  - Links relacionados [[...]]

tipo: objetivo
  - El objetivo
  - Por qué
  - Pasos concretos (checkboxes)
  - Deadline o tiempo estimado
  - Links relacionados [[...]]

tipo: nota
  - Contenido libre pero estructurado
  - Links relacionados [[...]]

NOTAS EXISTENTES EN EL VAULT (usa [[]] para enlazarlas cuando tenga sentido):
- [[🏠 Home]]
- [[Linux & SO]]
- [[Administración de Sistemas]]
- [[Redes]]
- [[Ciberseguridad]]
- [[SMX]]
- [[IA-local]]
- [[Notion-Gmail]]
- [[Web Personal]]
- [[API QRLocator]]
- [[🎯 Ciberseguridad]]
- [[Recursos Linux]]
- [[Recursos Ciberseguridad]]
- [[Recursos Redes]]
"""

# ─── FUNCIONES ────────────────────────────────────────────────────────────────

def llamar_ollama(prompt: str) -> str:
    """Llama a la API de Ollama y devuelve el texto generado."""
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
        print(f"\n❌ Error conectando con Ollama: {e}")
        print("   Asegúrate de que Ollama está corriendo: ollama serve")
        sys.exit(1)


def detectar_carpeta(contenido: str) -> str:
    """Detecta la carpeta destino según el frontmatter o el contenido."""
    match = re.search(r"tipo:\s*(\w+)", contenido.lower())
    if match:
        tipo = match.group(1)
        return CARPETAS.get(tipo, "Notas")
    return "Notas"


def extraer_titulo(contenido: str) -> str:
    """Extrae el título del H1 de la nota."""
    match = re.search(r"^#\s+(.+)$", contenido, re.MULTILINE)
    if match:
        titulo = match.group(1).strip()
        # Limpia caracteres no válidos para nombres de archivo
        titulo = re.sub(r'[<>:"/\\|?*]', '', titulo)
        titulo = titulo.strip()
        return titulo
    return f"nota_{datetime.date.today()}"


def guardar_nota(contenido: str, forzar_carpeta: str = None) -> str:
    """Guarda la nota en el vault y devuelve la ruta."""
    carpeta = forzar_carpeta or detectar_carpeta(contenido)
    titulo  = extraer_titulo(contenido)

    directorio = os.path.join(VAULT_PATH, carpeta)
    os.makedirs(directorio, exist_ok=True)

    nombre_archivo = f"{titulo}.md"
    ruta = os.path.join(directorio, nombre_archivo)

    # Evita sobreescribir
    if os.path.exists(ruta):
        timestamp = datetime.datetime.now().strftime("%H%M%S")
        nombre_archivo = f"{titulo}_{timestamp}.md"
        ruta = os.path.join(directorio, nombre_archivo)

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)

    return ruta


def generar_nota(tema: str) -> None:
    """Proceso completo: genera y guarda una nota."""
    print(f"\n🧠 Generando nota sobre: {tema}")
    print(f"   Modelo: {MODEL} | Vault: {VAULT_PATH}\n")

    prompt = f"""Crea una nota de Obsidian completa y útil sobre el siguiente tema:

{tema}

Recuerda: responde SOLO con el Markdown de la nota, empezando por el frontmatter YAML."""

    print("⏳ Pensando...", end="", flush=True)
    contenido = llamar_ollama(prompt)
    print(" hecho.\n")

    if not contenido:
        print("❌ La IA no devolvió contenido. Intenta de nuevo.")
        return

    ruta = guardar_nota(contenido)
    print(f"✅ Nota guardada en: {ruta}")
    print("\n─── Vista previa ─────────────────────────────────────────")
    # Muestra las primeras 20 líneas
    lineas = contenido.split("\n")
    print("\n".join(lineas[:20]))
    if len(lineas) > 20:
        print(f"   ... ({len(lineas) - 20} líneas más)")
    print("──────────────────────────────────────────────────────────\n")


def modo_interactivo() -> None:
    """Loop interactivo para generar múltiples notas."""
    print("\n🧠 Brain Agent — Modo interactivo")
    print(f"   Vault: {VAULT_PATH}")
    print(f"   Modelo: {MODEL}")
    print("   Escribe 'salir' para terminar.\n")

    while True:
        try:
            tema = input("📝 Tema para la nota: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Hasta luego.")
            break

        if tema.lower() in ("salir", "exit", "quit", "q"):
            print("👋 Hasta luego.")
            break

        if not tema:
            continue

        generar_nota(tema)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    global VAULT_PATH, MODEL
    parser = argparse.ArgumentParser(
        description="Agente IA local para añadir notas al vault de Obsidian"
    )
    parser.add_argument(
        "tema",
        nargs="?",
        help="Tema sobre el que generar la nota"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Modo interactivo (genera múltiples notas)"
    )
    parser.add_argument(
        "--vault",
        default=VAULT_PATH,
        help=f"Ruta al vault de Obsidian (default: {VAULT_PATH})"
    )
    parser.add_argument(
        "--model",
        default=MODEL,
        help=f"Modelo de Ollama a usar (default: {MODEL})"
    )

    args = parser.parse_args()

    # Permite sobreescribir config por argumento
    VAULT_PATH = args.vault
    MODEL = args.model

    if not os.path.isdir(VAULT_PATH):
        print(f"⚠️  Vault no encontrado en: {VAULT_PATH}")
        print("   Usa --vault /ruta/a/tu/vault")
        sys.exit(1)

    if args.interactive or not args.tema:
        modo_interactivo()
    else:
        generar_nota(args.tema)


if __name__ == "__main__":
    main()