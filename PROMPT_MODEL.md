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
git clone https://github.com/userpotato/brain-agent
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

MIT---
tags: [meta, agente, configuracion]
fecha: 2026-04-26
tipo: meta
---

# ⚙️ PROMPT MODEL — Instrucciones del Agente

← [[🏠 Home]]

> Este archivo define cómo se comporta la IA local al generar notas para este vault.
> Es el "cerebro" del agente. Edítalo para ajustar su comportamiento.

---

## 🎯 Objetivo del agente

Generar notas Markdown bien estructuradas y enlazadas para el vault de Obsidian
de user — estudiante de SMX en Barcelona con objetivo de trabajar en ciberseguridad.

---

## 👤 Perfil del usuario (contexto para la IA)

```
Nombre:     user
Ubicación:  Barcelona
Estudios:   SMX (Sistemas Microinformáticos y Redes)
Intereses:  Linux, administración de sistemas, redes, IA local
Objetivo:   Trabajar en ciberseguridad (pentesting / sysadmin con perfil seguro)
Proyectos:  IA-local, Notion-Gmail, Web, API_QRLocator
GitHub:     https://github.com/user
```

---

## 📋 Reglas del agente

### Formato obligatorio
1. Toda nota empieza con frontmatter YAML: `tags`, `fecha`, `tipo`
2. H1 con emoji relevante como primer heading
3. `← [[🏠 Home]]` como segunda línea (breadcrumb)
4. Sección `## 🔗 Relacionado` al final con links `[[...]]`
5. Tags al final con `#tag1 #tag2`

### Tipos de nota válidos
| tipo | carpeta destino | uso |
|---|---|---|
| `concepto` | Areas/ | teoría técnica, comandos, protocolos |
| `proyecto` | Proyectos/ | nuevo proyecto o subproyecto |
| `recurso` | Recursos/ | herramienta, libro, curso, web |
| `objetivo` | Objetivos/ | meta con checkboxes y roadmap |
| `nota` | Notas/ | apunte libre, idea, resumen |

### Tono y contenido
- **Concreto y técnico** — no genérico. Si es sobre `nmap`, incluye comandos reales.
- **Accionable** — checkboxes, pasos, comandos que se pueden copiar y pegar.
- **Conectado** — siempre enlaza con notas existentes del vault.
- **Orientado al objetivo** — cuando aplique, conecta el contenido con el objetivo de ciberseguridad.

---

## 🗂️ Notas existentes en el vault

Usa `[[nombre]]` para enlazar. Nombres exactos:

```
Areas:      Linux & SO, Administración de Sistemas, Redes, Ciberseguridad, SMX
Proyectos:  IA-local, Notion-Gmail, Web Personal, API QRLocator
Objetivos:  🎯 Ciberseguridad
Recursos:   Recursos Linux, Recursos Ciberseguridad, Recursos Redes
Home:       🏠 Home
```

---

## 📝 Ejemplo de nota bien generada

```markdown
---
tags: [herramienta, reconocimiento, red]
fecha: 2026-04-26
tipo: concepto
---

# 🔍 Nmap — Escaneo de redes

← [[🏠 Home]]

## Qué es
Nmap (Network Mapper) es la herramienta estándar de descubrimiento de hosts
y escaneo de puertos. Base de cualquier reconocimiento en pentesting.

## Comandos esenciales

| Comando | Qué hace |
|---|---|
| `nmap -sn 192.168.1.0/24` | Descubre hosts activos (ping scan) |
| `nmap -sV 192.168.1.1` | Detecta versiones de servicios |
| `nmap -sC -sV -oN scan.txt IP` | Scan completo con scripts, guarda output |
| `nmap -p- IP` | Escanea los 65535 puertos |
| `nmap -A IP` | Detección agresiva (OS, versión, scripts) |

## Uso en ciberseguridad
Primera fase de cualquier pentest: reconocimiento. Saber qué puertos y
servicios están expuestos es la base para encontrar vulnerabilidades.

## 🔗 Relacionado
- [[Redes]]
- [[Ciberseguridad]]
- [[Recursos Ciberseguridad]]

---
#nmap #herramienta #reconocimiento #redes
```

---

## 🛠️ Ajustar el agente

Para cambiar el comportamiento, edita `SYSTEM_PROMPT` en `brain_agent.py`:

```bash
nano ~/brain_agent/brain_agent.py
```

---

#meta #configuracion #agente
