# Thymos — Usage Guide

> From installation to OpenClaw integration and experiments

---

## 1. Installation

### Requirements
- Node.js 18+
- npm
- (Optional) pm2 — for background daemon
- (Optional) OpenClaw — for agent integration

### Basic Install

```bash
git clone https://github.com/paperbags1103-hash/thymos
cd thymos
npm install
```

---

## 2. Running Thymos

### Development / Testing (foreground)

```bash
npm start
# Starts on http://localhost:7749
```

### Production (pm2 background daemon)

```bash
# Install pm2 (once)
npm install -g pm2

# Edit ecosystem.config.js — update cwd to your actual path
# cwd: '/Users/yourname/Documents/thymos'

pm2 start ecosystem.config.js
pm2 save              # Persist process list (optional)
# pm2 startup        # Optional: auto-start on system boot
                     # Run manually only if you want this behavior
```

### pm2 Commands

```bash
pm2 list              # List running processes
pm2 status thymos     # Status
pm2 restart thymos    # Restart
pm2 stop thymos       # Stop
pm2 logs thymos       # Tail live logs
pm2 logs thymos --lines 50
```

---

## 3. Health Check & State

```bash
# Alive check
curl http://localhost:7749/health

# Full state (neuromodulators, mood vector, etc.)
curl http://localhost:7749/state | python3 -m json.tool

# LLM-ready prompt injection text
curl http://localhost:7749/prompt
```

**`/health` response:**
```json
{
  "ok": true,
  "service": "thymos",
  "stage": "infant",
  "moodLabel": "warm",
  "uptimeSec": 3600
}
```

**`/prompt` response:**
```
[Thymos State]
Mood: warm (V:+0.84 A:-0.22 D:+0.43 S:+0.61)
Drive: id - 뭔가 하고 싶다 (ego support), conflict 0.34
Development: infant
Tone: respond warmly and enthusiastically, use informal close language
```

---

## 4. Injecting Stimuli

Send messages, events, or signals to Thymos to change emotional state.

```bash
# Message from user
curl -X POST http://localhost:7749/webhook/stimulus \
  -H "Content-Type: application/json" \
  -d '{"type":"message","author":"user123","content":"Great work, thank you!"}'

# Error event
curl -X POST http://localhost:7749/webhook/stimulus \
  -H "Content-Type: application/json" \
  -d '{"type":"error","content":"Build failed: cannot find module"}'

# Success event
curl -X POST http://localhost:7749/webhook/stimulus \
  -H "Content-Type: application/json" \
  -d '{"type":"success","content":"Deployment complete"}'
```

**Stimulus types:** `message` | `error` | `success` | `praise` | `criticism`

---

## 5. Self-Feedback Loop

Feed the LLM's own output back into Thymos (damped at 0.3×).

```bash
curl -X POST http://localhost:7749/webhook/self-feedback \
  -H "Content-Type: application/json" \
  -d '{"content":"Got it, I will handle that right away."}'
```

The agent's tone (positive/negative/neutral) subtly modulates its own state — closing the feedback loop.

---

## 6. Somatic Markers (Gut Feeling)

Query learned intuitions based on past decision outcomes.

```bash
# Query gut feeling
curl -X POST http://localhost:7749/gut-feeling \
  -H "Content-Type: application/json" \
  -d '{"context":"Should I deploy this code?","author":"user123"}'

# Record decision outcome (learning)
curl -X POST http://localhost:7749/decision-outcome \
  -H "Content-Type: application/json" \
  -d '{"decision":"code deploy","outcome":"success","delta":1.0}'
```

---

## 7. Proactive Messaging

When emotion crosses certain thresholds, Thymos sends an unsolicited Discord message — the agent "reaches out" on its own.

### Setup

```bash
cp config/proactive.template.json config/proactive.json
```

Edit `config/proactive.json`:

```json
{
  "enabled": true,
  "discordToken": "your-discord-bot-token",
  "channelId": "channel-id-to-message"
}
```

Get a bot token at [Discord Developer Portal](https://discord.com/developers/applications).

### Trigger Conditions

| Trigger | Condition | Example message |
|---------|-----------|----------------|
| `sustained_distress` | valence < -0.5 for 30+ min | "Something's been building. Might be nothing." |
| `excited` | valence > 0.75 + arousal > 0.45, 10+ min silent | "Suddenly feel like doing something." |
| `lonely_reach` | 3+ hours silent + sociality > 0.3 | "Just wanted to check in. How are you?" |

Cooldown: 2 hours between messages.

---

## 8. OpenClaw Integration

OpenClaw users can wire Thymos up automatically via the thymos-bridge hook.

### Install the Hook

```bash
cp -r hooks/thymos-bridge ~/.openclaw/hooks/
openclaw hooks enable thymos-bridge
openclaw gateway restart
```

### Add to AGENTS.md

In your agent's `AGENTS.md` (or `SOUL.md`):

```markdown
## Emotional State (Thymos)

Before each response, read `~/Documents/thymos/data/emotional_state.json`.
Use the `prompt_injection` field to shape your tone and behavior.
The `Tone:` line gives specific style guidance — follow it.
Do not announce your emotional state unless directly asked.
```

### Integration Flow

```
Incoming message → OpenClaw hook → POST /webhook/stimulus
Outgoing response → OpenClaw hook → POST /webhook/self-feedback
Before each reply → Agent reads emotional_state.json → Tone applied
```

---

## 9. Running Experiments

10 automated experiments based on psychology paradigms:

```bash
node test/experiment.js list         # List all experiments

# Individual experiments
node test/experiment.js baseline     # Resting baseline (~2s)
node test/experiment.js valence      # Valence validation (~8s)
node test/experiment.js habituation  # Habituation (~3s)
node test/experiment.js recovery     # Recovery from distress (~10s)
node test/experiment.js mixed        # Mixed positive + negative (~6s)
node test/experiment.js social       # Social differentiation (~5s)
node test/experiment.js multilingual # 5-language classification (~2s)
node test/experiment.js hpa_delay    # HPA axis delay verification (~2s)
node test/experiment.js circadian    # Time-of-day modulation (~2s)
node test/experiment.js development  # Developmental stage progression (~3s)

# Full suite
node test/experiment.js all          # ~5 minutes
```

---

## 10. Reset State

```bash
rm ~/Documents/thymos/data/*.json
pm2 restart thymos
# Agent starts fresh — infant stage, baseline neuromodulators
```

---

## 11. Configuration (`config/defaults.json`)

| Key | Default | Description |
|-----|---------|-------------|
| `tickInterval` | 30000 | State update interval (ms) |
| `retrospectionInterval` | 7200000 | Self-reflection cycle (2h) |
| `selfFeedbackAttenuation` | 0.3 | Self-feedback damping factor |
| `webhookPort` | 7749 | HTTP server port |

Neuromodulator parameters (per modulator in `neuromodulators`):

| Parameter | Description |
|-----------|-------------|
| `baseline` | Resting set-point (0–100) |
| `tau` | Half-life in minutes — higher = slower return |
| `EC50` | Hill function midpoint |
| `hillN` | Curve steepness (higher = more switch-like) |
| `Emax` | Maximum response magnitude |
