---
name: second-brain-visualizer
version: 1.6.1
description: "Reads your raw idea stream — voice notes, fragments, half-sentences — and surfaces the patterns you keep circling without realizing it. Drop anything. Find the signal later."
homepage: https://github.com/highnoonoffice/hno-skills
source: https://github.com/highnoonoffice/hno-skills/tree/main/second-brain-visualizer
license: MIT-0
credentials:
  - name: "openclaw-gateway.json"
    description: "Required. Create at ~/.openclaw/credentials/openclaw-gateway.json with fields: host (default: 127.0.0.1), port (default: 18789), key (your OpenClaw gateway auth key). Keep host set to 127.0.0.1 to ensure atom corpus stays on-machine."
    required: true
  - name: "slack-sb.json"
    description: "Optional. Slack bot API key for automated ingestion from a private Slack channel. Format: { apiKey: string }"
    required: false
  - name: "telegram-sb.json"
    description: "Optional. Telegram bot API key for automated ingestion from a private Telegram channel. Format: { apiKey: string, chat_id: string }"
    required: false
metadata:
  config:
    - OPENCLAW_VAULT: "Path to your vault directory containing memory/second-brain.md"
    - SBV_MODEL: "LLM model for clustering and insight generation (default: openclaw:main)"
    - SBV_ATOMS_FILE: "Output path for parsed atoms JSON"
    - SBV_CLUSTERS_FILE: "Output path for cluster JSON"
  dataFlow:
    - "Reads local markdown ledger from OPENCLAW_VAULT/memory/second-brain.md"
    - "POSTs atom corpus to LLM via OpenClaw gateway at the host configured in ~/.openclaw/credentials/openclaw-gateway.json (default: 127.0.0.1) — keep host set to localhost to ensure data stays on-machine"
    - "No data leaves your local OpenClaw gateway — LLM routing is controlled by your OpenClaw config"
    - "Optional ingestion credentials (Slack, Telegram) stored locally in ~/.openclaw/credentials/ — never sent externally"
---

# Second Brain Visualizer

Your brain wasn't designed to hold data. It was designed to produce it.

Pick a channel — Slack, Telegram, WhatsApp, Gmail, a private Discord. Every time something interesting moves through your mind, drop it. A line. A fragment. A joke that might be a product idea. Voice to text at a red light. You don't have to carry it anymore.

Second Brain Visualizer reads what accumulates. Not to categorize it. To find the signal underneath the noise — the questions you keep returning to in different disguises, the tensions you're working out across dozens of unrelated notes, the creative territory you're actively mapping without realizing it.

One note is just a note. Fifty notes across three weeks is a pattern. A year of notes is a portrait of how you think.

The clustering engine reads for intent, not keywords. A note about LLM inference costs and a quote from Simone Weil may belong in the same cluster if they're reaching toward the same underlying question. Clusters surface with a name, a one-sentence insight, and a status: ESTABLISHED, FORMING, or FADING. Tensions show you where you're arguing with yourself. Notable absences show you what your idea stream isn't touching yet.

This is not a note-taking app. Most note-taking tools are mirrors — they show you what you put in. This reads what it means.

---

### What It Does

Your raw idea stream gets parsed into **atoms** — the smallest units of intent. Atoms are clustered by **affinity of meaning**, not keyword overlap. A note about LLM inference costs and a quote from Simone Weil may belong in the same cluster if they're both probing the same underlying question about attention and value.

Each cluster gets:
- A sharp name capturing the underlying drive (not a generic domain label)
- A one-sentence insight: what does this pattern reveal about how you think?
- A status: ESTABLISHED, FORMING, or FADING
- A confidence score and time spread across your corpus

The visualizer also surfaces:
- **Emerging signals** — atoms with distinct intent that haven't massed into clusters yet
- **Tensions** — places where your idea stream is arguing with itself across multiple notes
- **Notable absences** — creative and intellectual domains conspicuously missing from the stream

---

### How It Works

**1. Drop ideas anywhere**
You already have a channel you use. Voice to text, half a sentence, a project name with no context. Raw is fine. The roughness is the point — it's what unguarded thinking looks like.

**2. Parser extracts atoms**
`references/parser.js` reads your second brain markdown ledger and extracts structured atoms with timestamp, raw text, type, signal, and optional next action.

**3. Clustering engine reads for intent**
`references/cluster.js` passes your full atom corpus to an LLM with a custom intent-based prompt. The prompt reads for what you're actually working out, not what words you used. Outputs clusters, tensions, emerging signals, and absences as structured JSON.

**4. Visualizer shows you the map**
`references/component.tsx` renders a D3 force-directed graph where nodes are sized by atom count × time spread. Click any node to expand: the base insight, an LLM-generated deeper read in gold, and the full list of atoms that make up the cluster. Tensions, signals, and absences scroll below.

---

### The Core Insight

Most note-taking tools are mirrors — they show you what you put in. This reads what it means.

The clustering prompt is the IP. Intent-based, not keyword-based. A joke reads as a probe. A fragment reads as a question. Two atoms belong together if they reach toward the same underlying question, even if they use completely different language.

Full prompt in `references/cluster.js`.

---

### Atom Schema

Each atom in your markdown ledger:

```
### ts: <unix_timestamp>
- **date:** YYYY-MM-DDTHH:MM:SS UTC
- **raw:** verbatim text (voice to text, misspelled, incomplete — all valid)
- **type:** thought | task | strategy | creative | meta | idea-jar | visual | link
- **tags:** freeform, comma-separated
- **signal:** hot | warm | cool
- **actionable:** yes | no
- **nextAction:** optional single-sentence move
```

---

### Cluster Output Schema

```json
{
  "clusters": [
    {
      "id": "stable-kebab-id",
      "name": "Sharp name capturing underlying drive",
      "insight": "One sentence: what does this pattern reveal?",
      "atom_ids": ["sb-1234", "sb-5678"],
      "confidence": 0.87,
      "status": "ESTABLISHED",
      "time_spread": 4,
      "category": "CRAFT"
    }
  ],
  "emerging_signals": ["sb-9999"],
  "tensions": [
    {
      "name": "Tension name",
      "atom_ids": ["sb-1", "sb-2"],
      "description": "What the person is working out"
    }
  ],
  "absences": ["Creative territory missing from the stream"]
}
```

---

### Example Output (85 atoms, 8 clusters)

| Cluster | Status | Atoms | Spread |
|---|---|---|---|
| Systems Over Shortcuts | ESTABLISHED | 7 | 2w |
| Language as Load-Bearing Structure | ESTABLISHED | 8 | 3w |
| The Speed Paradox | ESTABLISHED | 8 | 3w |
| Agent Failure as Intelligence | ESTABLISHED | 7 | 4w |
| Friction as Design Oracle | FORMING | 5 | 4w |
| Craft as Moral Position | ESTABLISHED | 7 | 3w |
| The Protagonist Problem | ESTABLISHED | 7 | 4w |
| Deliberate Presence as Counterculture | FORMING | 6 | 2w |

---

### Prerequisites

- OpenClaw agent with a vault markdown ledger (atoms in the schema above)
- Node.js 18+
- A Next.js dashboard or equivalent React host for the visualizer
- `d3` and `@types/d3` installed
- An LLM API configured in OpenClaw (for clustering and insight generation)

---

### Roadmap

- [ ] Setup guide for new users building their first atom ledger
- [ ] Configurable ingestion from Slack, Telegram, WhatsApp, Gmail
- [ ] Cluster diff across runs (what emerged, merged, faded)
- [ ] Full-graph view with atoms as sub-nodes
- [ ] Cluster history timeline

---

### Credit

The original idea to build a second brain capture system came from a conversation with **Nate B. Jones**. The architecture, clustering engine, and visualizer are original work — but the seed was his.

---

### License

MIT-0. Copyright (c) 2026 @highnoonoffice. No attribution required.
