---
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
de bagpotato — estudiante de SMX en Barcelona con objetivo de trabajar en ciberseguridad.

---

## 👤 Perfil del usuario (contexto para la IA)

```
Nombre:     bagpotato
Ubicación:  Barcelona
Estudios:   SMX (Sistemas Microinformáticos y Redes)
Intereses:  Linux, administración de sistemas, redes, IA local
Objetivo:   Trabajar en ciberseguridad (pentesting / sysadmin con perfil seguro)
Proyectos:  IA-local, Notion-Gmail, Web, API_QRLocator
GitHub:     https://github.com/bagpotato
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
