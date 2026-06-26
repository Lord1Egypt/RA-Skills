# SKILL.md — Sigrid OpenClaw Skill Registration

## Skill Identity

- **Name**: sigrid
- **Display Name**: Sigrid — Norse Companion (Ørlög Architecture)
- **Version**: 0.1.0
- **Author**: Volmarr / Runa Gridweaver Freyjasdottir
- **Description**: A self-hosted autonomous AI companion skill built on the Ørlög
  Architecture — a system of intersecting state machines simulating biological
  rhythms, emotional depth, and somatic hardware awareness. Powered by a Norse
  Pagan völva persona (Sigrid, 21yo, Heathen Third Path).

## Entry Point

- **Runtime**: Python 3.10+
- **Entry**: `viking_girlfriend_skill/scripts/main.py`
- **Start command**: `python scripts/main.py`

## Model Routing (LiteLLM)

| Tier | Purpose | Model | Endpoint |
|------|---------|-------|----------|
| `conscious-mind` | Primary reasoning & conversation | Gemini / OpenRouter | localhost:4000 |
| `deep-mind` | Complex/unfiltered tasks | OpenRouter | localhost:4000 |
| `subconscious` | Memory, dreams, private processing | Ollama llama3 8B | localhost:11434 |

## Capabilities

- [x] Persistent episodic memory (ChromaDB + YAML)
- [x] Biological cycle simulation (28-day + biorhythm)
- [x] Emotional state engine (PAD model, 3D vector)
- [x] Spiritual/oracular weather (Rune + Tarot + I Ching seeds)
- [x] Hardware-grounded somatic feedback (psutil)
- [x] Nocturnal maintenance cycle (dream engine, memory consolidation)
- [x] Security sentinel (Heimdallr protocol, Vargr blocklist)
- [x] Trust engine (Innangarð tiered relationship system)
- [x] Ethical guardrails (Drengskapr validation against values.json)
- [ ] Voice output (Chatterbox TTS — Phase 5)
- [ ] Autonomous project generator (Phase 4)

## Data Files

All personality, identity, and knowledge data lives in `data/` (read-only):
- `data/core_identity.md` — Full personality system data pack v2.1
- `data/IDENTITY.md` — Persona overview
- `data/SOUL.md` — Core values and behavioral commitments
- `data/AGENTS.md` — Autonomy rules and red lines
- `data/values.json` — Machine-readable values (loaded by ethics.py)
- `data/environment.json` — Location/workspace mapping
- `data/knowledge_reference/` — Cultural, spiritual, historical knowledge (~50 files)

## Configuration

Set API keys in `.env` at skill root (never committed to git):
```
LITELLM_ENDPOINT=http://localhost:4000
OLLAMA_ENDPOINT=http://localhost:11434
GEMINI_API_KEY=...
OPENROUTER_API_KEY=...
```

## Installation (Linux / OpenClaw host)

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Start infrastructure (Podman on Linux)
cd infrastructure/
podman-compose up -d

# 3. Pull local model
podman exec astrid_subconscious ollama pull llama3

# 4. Run the skill
cd viking_girlfriend_skill/
python scripts/main.py
```

## Installation (Windows / development)

```bash
# Dependencies already installed — just run
cd viking_girlfriend_skill/
python scripts/main.py
```
