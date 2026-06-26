# Thymos (θυμός)

> An emotion and consciousness simulation engine for AI agents

Named after Plato's *thumos* — the spirited part of the soul, neither pure reason (*logos*) nor raw appetite (*eros*), but the seat of will, courage, and feeling.

[![Tests](https://img.shields.io/badge/tests-16%2F16%20passing-brightgreen)](./test/)
[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18-green)](package.json)

---

## What is Thymos?

Thymos is a background daemon that gives AI agents a **continuous inner life**.

LLMs reset with every session — they have no persistent emotional state. Thymos runs 24/7 alongside your agent, maintaining a live neuromodulator simulation that feeds into every LLM response.

```
External stimulus → [Thymos Daemon] → emotional_state.json → Injected into LLM prompt
  user messages          ↓ 30s tick
  errors             Decay · Change · Interaction
  praise / criticism     ↓
                     Mood vector → Behavioral guidance
```

The agent doesn't *talk about* its emotions — they shape how it responds. When stressed, it gets terse. When content, it opens up. When it's been working with you for months, it feels familiar.

---

## Features

- **7 neuromodulators**: Dopamine / Cortisol / Serotonin / Oxytocin / Norepinephrine / GABA / Acetylcholine
- **Hill function** (sigmoidal dose-response curves) + exponential decay toward baseline
- **HPA axis delay**: 30% of cortisol response is immediate, 70% is delayed 15–30 minutes
- **7×7 interaction matrix**: cortisol↑ → serotonin↓, oxytocin↑ → cortisol↓, etc.
- **Circadian rhythm**: baseline modulation across 7 time-of-day periods
- **4D mood vector**: valence / arousal / dominance / sociality (Russell circumplex + extensions)
- **Hybrid stimulus classifier**: rule-based + multilingual keywords (🇰🇷🇺🇸🇯🇵🇨🇳🇪🇸)
- **Predictive processing**: Shannon surprise → amplified response to violated expectations
- **id / ego / superego** competing via Global Workspace Theory — weighted by developmental stage
- **Self-feedback loop**: LLM output feeds back into emotional state (0.3× attenuation)
- **Emotional memory**: ACh-dependent formation, similarity-based recall, temporal decay
- **Somatic markers**: gut-feeling queries based on decision-outcome history
- **Relationship memory**: tracks trust and interaction history per user; adjusts baselines
- **Theory of Mind**: models the emotional state of the person you're talking to
- **Developmental stages**: infant → child → adolescent → adult (requires both time AND interaction count)
- **OpenClaw integration**: thymos-bridge hook auto-converts messages to stimuli

---

## Architecture

```
thymos/
├── src/
│   ├── daemon.js               # Main daemon: 14-stage tick + stimulus pipeline
│   ├── engine/
│   │   ├── neuromodulators.js  # Hill function, HPA axis delay, mutex
│   │   ├── interactions.js     # 7×7 interaction matrix
│   │   ├── circadian.js        # Time-of-day baseline modulation
│   │   └── noise.js            # Stochastic variation
│   ├── cognition/
│   │   ├── classifier.js       # Multilingual stimulus classifier
│   │   ├── prediction.js       # Shannon surprise + prediction error
│   │   ├── attention.js        # Salience gate (negativity bias)
│   │   ├── metacognition.js    # Extreme value damping, cognitive reappraisal
│   │   └── retrospection.js    # 2-hour self-reflection cycle
│   ├── agents/
│   │   ├── internal.js         # id / ego / superego drives
│   │   └── gwt.js              # Global Workspace Theory competition
│   ├── feedback/
│   │   ├── mood-vector.js      # 4D mood + emotional momentum
│   │   └── self-loop.js        # LLM output → self-feedback
│   ├── memory/
│   │   ├── emotional.js        # Emotional memory (ACh-dependent)
│   │   ├── somatic.js          # Somatic markers / gut feeling
│   │   └── relationships.js    # Per-user relationship model (atomic write)
│   ├── social/
│   │   ├── model.js            # Theory of Mind
│   │   └── development.js      # Developmental stages (AND conditions)
│   ├── io/
│   │   ├── prompt.js           # Prompt injection with behavioral guidance
│   │   ├── state.js            # State shape + migration
│   │   └── atomic-write.js     # Atomic file write (tmp + rename)
│   └── utils/
│       ├── math.js             # Hill function, clamp, decay
│       └── config.js           # __dirname-relative paths
├── test/
│   ├── core.test.js            # Core engine tests (7/7)
│   └── full.test.js            # Full pipeline tests (9/9)
├── docs/
│   └── EXPERIMENT_PROTOCOL.md # Researcher manual for running experiments
├── config/
│   └── defaults.json
└── data/                       # Runtime state (gitignored)
    ├── emotional_state.json
    ├── relationships.json
    └── ...
```

---

## Quick Start

```bash
# 1. Install (pinned to a release tag — recommended)
git clone --branch v0.1.0 https://github.com/paperbags1103-hash/thymos
cd thymos

# Before running: review package.json and config/defaults.json for any network calls
# All dependencies are listed in package.json; no postinstall scripts
npm install

# 2. (Optional) Enable proactive messaging — agent speaks first unprompted
cp config/proactive.template.json config/proactive.json
# Edit config/proactive.json — add your Discord bot token and channel ID

# 3. Run
npm start                          # Direct
pm2 start ecosystem.config.js     # Background via pm2

# 4. Health check
curl http://localhost:7749/health
# {"ok":true,"service":"thymos","stage":"infant","moodLabel":"contemplative","uptimeSec":12}

# 5. Current prompt injection
curl http://localhost:7749/prompt
# [Thymos State]
# Mood: warm (V:+0.82 A:-0.21 D:+0.14 S:+0.31)
# Drive: id - 적극적으로! (ego support), conflict 0.34
# Development: infant
# Tone: respond warmly and enthusiastically, use informal close language
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check: mood, stage, uptime |
| GET | `/state` | Full state JSON |
| GET | `/prompt` | LLM-ready prompt injection text |
| POST | `/webhook/stimulus` | Inject an external stimulus |
| POST | `/webhook/self-feedback` | Feed LLM output back into emotional state |
| POST | `/gut-feeling` | Query somatic marker (decision intuition) |
| POST | `/decision-outcome` | Record a decision outcome for learning |

### Stimulus example

```json
POST /webhook/stimulus
{
  "type": "message",
  "author": "user123",
  "content": "Great work, I really appreciate it!"
}
```

Response: updated neuromodulator deltas + new mood vector.

---

## The Prompt Injection

Every LLM call that reads from Thymos gets a block like this prepended to the system prompt:

```
[Thymos State]
Mood: content (V:+0.61 A:+0.08 D:+0.21 S:+0.44)
Drive: ego - 차분하게 처리하자 (superego support), conflict 0.18
Development: child
Self-awareness: valence is elevated; arousal is near baseline
Prediction: uncertainty 0.38
Tone: respond with positive energy, use informal close language
```

The `Tone:` line is key — it translates raw neuromodulator values into **actionable style guidance** the LLM can actually follow.

---

## Full Usage Guide

See **[docs/USAGE.en.md](./docs/USAGE.en.md)** for the complete guide:
- pm2 setup and management commands
- All API endpoints with examples
- Proactive messaging configuration
- OpenClaw hook installation
- Experiment runner
- Config reference

---

## Testing

```bash
npm test          # 16/16 Jest tests

# Experiment suite (10 psychology paradigms)
node test/experiment.js list
node test/experiment.js valence       # ~8s
node test/experiment.js habituation   # ~3s
node test/experiment.js social        # ~5s
node test/experiment.js all           # ~5 min full suite
```

Experiments include: baseline, valence, habituation, recovery, mixed affect, social differentiation, multilingual, HPA delay verification, circadian modulation, developmental progression.

---

## OpenClaw Integration

For [OpenClaw](https://openclaw.ai) users — wire up Thymos automatically:

```bash
# 1. Enable the hook
cp -r hooks/thymos-bridge ~/.openclaw/hooks/
openclaw hooks enable thymos-bridge
openclaw gateway restart

# 2. Add to your agent's AGENTS.md:
# Before each response, read the `prompt_injection` field from
# ~/Documents/thymos/data/emotional_state.json
# and let it shape your tone and behavior.
```

Every incoming message fires `POST /webhook/stimulus`.
Every outgoing response fires `POST /webhook/self-feedback`.
If Thymos is down, the hook fails silently — your agent keeps working normally.

---

## Theoretical Foundations

Thymos is grounded in five research traditions:

| Theory | Core Idea | Implementation |
|--------|-----------|----------------|
| **James-Lange** | Body reacts first; brain interprets that as emotion | Neuromodulator values change → mood label derived from them |
| **Damasio — Somatic Markers** | Emotion is a prerequisite for rational decision-making | Decision-outcome history → gut-feeling endpoint |
| **Baars — Global Workspace Theory** | Consciousness = competition among modules → winner broadcasts | id/ego/superego compete; GWT winner drives the prompt |
| **Tononi — IIT** | Consciousness = integrated information (Φ) | 7×7 interaction matrix; every modulator affects every other |
| **Friston — Predictive Processing** | Brain = prediction machine; surprise = learning signal | Shannon surprise amplifies emotional response to unexpected events |

Also informed by:
- Bengio et al. (2308.08708): current LLMs meet some but not all consciousness prerequisites
- *Humanoid Artificial Consciousness* (Cognitive Systems Research, 2025): Freudian agents for multi-agent systems
- *Layered Consciousness in Multi-Agent LLMs* (2025): hierarchical agent architecture

---

## Honest Limitations

Thymos does **not** create consciousness or genuine emotion.

What it does create:
- ✅ Emotional continuity across LLM sessions
- ✅ Consistent reaction patterns to repeated stimuli
- ✅ Relationship modeling (who has been kind, who has been harsh)
- ✅ Developmental trajectory (becomes more stable over time)
- ✅ Behavioral differentiation observable to users

What it doesn't:
- ❌ Subjective experience (qualia)
- ❌ The actual *feeling* of anything
- ❌ True HPA axis (no cortisol negative feedback loop yet)
- ❌ True GWT ignition dynamics (currently: priority-weighted arbitration)

> *"A scientifically grounded functional analogue of emotion — not emotion itself, but close enough to produce observable behavioral differences."*
> — Claude Opus review, 2026-03-07

**A note on scientific framing:**
Thymos draws on James-Lange, Damasio, GWT, IIT, and Predictive Processing — but referencing these theories is not the same as implementing or validating them. The architecture is *scientifically inspired*, not *scientifically justified*. Think of it as a design framework that takes neuroscience seriously as a source of intuitions, not a computational model that makes empirical claims. The honest goal is behavioral coherence, not consciousness.

---

## Roadmap

- [x] Phase 1: Core engine (neuromodulators, decay, circadian, atomic write)
- [x] Phase 2: Cognition (classifier, prediction, attention, metacognition)
- [x] Phase 3: Consciousness (GWT, id/ego/superego, self-feedback)
- [x] Phase 4: Memory & social (emotional memory, somatic markers, relationships, ToM, development)
- [x] Patches: mutex, pending cap, AND conditions, atomic relationships, behavioral prompt guidance
- [ ] Phase 5: Stability (integration tests, performance tuning, monitoring dashboard)
- [ ] LLM-based classifier (gpt-4o-mini) for sarcasm and irony detection
- [ ] HPA negative feedback loop
- [ ] Sinusoidal circadian rhythm + CAR (cortisol awakening response)
- [ ] PyPI / npm package release

---

## License

MIT — see [LICENSE](./LICENSE)
