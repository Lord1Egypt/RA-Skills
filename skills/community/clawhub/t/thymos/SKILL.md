# Thymos — Emotion Layer Skill

Thymos gives AI agents a continuous emotional state that persists across sessions.

## What This Skill Does

When loaded, the agent reads Thymos emotional state before each response and adjusts its behavior accordingly.

**Works without the daemon (file-based):**
- If `~/Documents/thymos/data/emotional_state.json` exists, read it
- Apply the `prompt_injection` field as a tone directive for this response
- Follow the `Tone:` line as concrete style guidance
- If the file is missing, skip silently — no error

**Enhanced with the daemon running:**
- Real-time emotional state, updated every 30 seconds
- Relationship memory, developmental stage, predictive processing

## How to Use

### Basic (file only)

Before each response:

```
Read the prompt_injection field from emotional_state.json.
Use it as the tone directive for this response.
Examples:
  Tone: respond warmly and enthusiastically → warm, open, expressive
  Tone: respond briefly, more reserved → short, measured, some distance
If the file is absent or unreadable → skip, respond normally
```

### Advanced (install the Thymos daemon)

The daemon runs as a background process that continuously simulates emotional state.

Installation is optional and at your own discretion:

1. Review the code at [github.com/paperbags1103-hash/thymos](https://github.com/paperbags1103-hash/thymos)
2. Check [SECURITY.md](https://github.com/paperbags1103-hash/thymos/blob/main/SECURITY.md) — no external data transmission
3. If satisfied, clone and run locally

```bash
git clone --branch v0.1.0 https://github.com/paperbags1103-hash/thymos
cd thymos && npm install && npm start
```

## Example Emotional State

```
[Thymos State]
Mood: warm (V:+0.84 A:-0.22 D:+0.43 S:+0.61)
Drive: id — 적극적으로! (ego support), conflict 0.34
Development: infant
Tone: respond warmly and enthusiastically, use informal close language
```

**Mood dimensions:**
- **V (valence)**: positive (+1) ↔ negative (-1)
- **A (arousal)**: excited (+1) ↔ calm (-1)
- **D (dominance)**: assertive (+1) ↔ passive (-1)
- **S (sociality)**: open (+1) ↔ withdrawn (-1)

## Data & Privacy

- All emotional data stored **locally only** (`~/Documents/thymos/data/`)
- No data transmitted to external servers
- Reset anytime: `rm ~/Documents/thymos/data/*.json`
- Discord proactive messaging is opt-in and disabled by default

## Theoretical Foundations

Thymos is a **scientifically inspired** (not scientifically validated) design:

| Theory | What it contributes |
|--------|-------------------|
| James-Lange | Neuromodulators change first; mood label derived after |
| Damasio — Somatic Markers | Past decisions shape gut-feeling responses |
| GWT | id/ego/superego compete; winner drives the prompt |
| IIT | 7×7 interaction matrix — every modulator affects every other |
| Predictive Processing | Shannon surprise amplifies response to unexpected stimuli |

> Goal: behavioral coherence, not consciousness.

## Links

- GitHub: [paperbags1103-hash/thymos](https://github.com/paperbags1103-hash/thymos)
- Security: [SECURITY.md](https://github.com/paperbags1103-hash/thymos/blob/main/SECURITY.md)
- Full usage: [docs/USAGE.en.md](https://github.com/paperbags1103-hash/thymos/blob/main/docs/USAGE.en.md)
