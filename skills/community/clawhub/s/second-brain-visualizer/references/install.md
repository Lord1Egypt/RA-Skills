---
title: "Second Brain Visualizer — Install Guide"
version: 1.0.0
---

# Install Guide

## Prerequisites

Before you start, confirm you have:

- **OpenClaw** installed and running (`openclaw status` returns ok)
- **Node.js 18+** (`node --version`)
- **An LLM configured** in OpenClaw — any model works, but one with a 32k+ context window handles large atom corpora better. Maple, GPT-4o, Claude Sonnet, or Gemini 2.5 Pro all work.
- **A vault directory** — wherever OpenClaw stores your markdown files (`echo $OPENCLAW_VAULT` or check `~/.openclaw/` directory for your configured vault path)

---

## Step 1 — Clone the skill

```bash
git clone https://github.com/highnoonoffice/hno-skills.git
cd hno-skills/second-brain-visualizer
```

Or if you already have the hno-skills repo:

```bash
cd hno-skills && git pull origin main
cd second-brain-visualizer
```

---

## Step 2 — Create your atom ledger

In your vault's `memory/` directory, create `second-brain.md`:

```bash
cat > $OPENCLAW_VAULT/memory/second-brain.md << 'EOF'
---
title: "Second Brain — Atom Ledger"
created: $(date +%Y-%m-%d)
tags: [second-brain, ideas, capture]
status: active
---

# Second Brain — What It Is

A raw idea capture tool. Not a journal. Not a task list.
EOF
```

See `references/setup.md` for how to write your first atoms manually, or `references/ingestion.md` to wire up automated ingestion from Slack, Telegram, or another channel.

---

## Step 3 — Configure paths in the scripts

Open `references/parser.js` and set your vault path:

```javascript
// Line 10 — set this to your vault directory
const VAULT = process.env.OPENCLAW_VAULT || '/path/to/your/vault';
```

Open `references/cluster.js` and set your LLM endpoint:

```javascript
// Line 15 — set your OpenClaw gateway URL
const GATEWAY = process.env.OPENCLAW_GATEWAY || 'http://127.0.0.1:18789';

// Line 16 — set your preferred model
const MODEL = process.env.SBV_MODEL || 'maple/gpt-oss-120b';
```

Or set environment variables instead of editing the files:

```bash
export OPENCLAW_VAULT="/Users/yourname/.openclaw/vault"
export OPENCLAW_GATEWAY="http://127.0.0.1:18789"
export SBV_MODEL="maple/gpt-oss-120b"
```

---

## Step 4 — Set up output directories

The scripts write to your Mission Control data directory. Create it if it doesn't exist:

```bash
mkdir -p /path/to/your/mission-control/data
```

Then update the output paths in `parser.js` and `cluster.js`:

```javascript
// parser.js — Line 13
const OUT_FILE = '/path/to/your/mission-control/data/second-brain-atoms.json';

// cluster.js — Line 17
const ATOMS_FILE = '/path/to/your/mission-control/data/second-brain-atoms.json';
const OUT_FILE   = '/path/to/your/mission-control/data/second-brain-clusters.json';
```

---

## Step 5 — Run the parser

```bash
node references/parser.js
```

Expected output:

```
Parsed 42 atoms → /path/to/data/second-brain-atoms.json
```

If you see `0 atoms parsed`, your ledger may be empty or the format doesn't match what the parser expects. See `references/setup.md` for the atom format.

---

## Step 6 — Run clustering

```bash
node references/cluster.js
```

This will take 20–60 seconds on first run (LLM call with full corpus). Expected output:

```
Clustering 42 atoms…
✓ 6 clusters written to /path/to/data/second-brain-clusters.json
  [ESTABLISHED] The Legitimacy Project — 8 atoms, 3w spread
  [ESTABLISHED] Language as Load-Bearing Structure — 7 atoms, 4w spread
  [FORMING] Friction as Design Oracle — 4 atoms, 2w spread
  ...
  3 emerging signals
  2 tensions
```

---

## Step 7 — Mount the React component

The visualizer is a React component (`references/component.tsx`) that reads from the two JSON files produced above.

**If you're using Mission Control or a similar Next.js dashboard:**

1. Copy `references/component.tsx` into your `components/tabs/` directory
2. Import and register it as a tab in your sidebar nav
3. Add API routes that serve `second-brain-atoms.json` and `second-brain-clusters.json`
4. Add an insight generation route (POST endpoint that calls your LLM with a cluster's atoms)

The component expects three API endpoints:

```
GET  /api/second-brain/atoms     → { atoms: [...] }
GET  /api/second-brain/clusters  → { clusters: [...], tensions: [...], absences: [...], ... }
POST /api/second-brain/clusters  → triggers re-clustering, returns new clusters
POST /api/second-brain/insight   → { atom_texts: [...], cluster_name: string } → { insight: string }
```

**If you're running standalone (no dashboard):**

Wrap the component in a minimal Next.js or Vite app. The component is self-contained — it only needs D3 and the four API endpoints above.

---

## Step 8 — Install frontend dependencies

In your dashboard project:

```bash
npm install d3
npm install --save-dev @types/d3
```

---

## Verify the full pipeline

1. Parser runs and outputs atoms ✓
2. Clusterer runs and outputs clusters ✓
3. Component loads in browser ✓
4. Clicking a node opens its detail panel ✓
5. Re-cluster button triggers a fresh LLM call ✓

If all five work, you're running. Drop 10 more ideas into your channel, re-ingest, re-cluster, and watch the graph shift.

---

## Environment variable reference

| Variable | Default | Description |
|---|---|---|
| `OPENCLAW_VAULT` | `/path/to/vault` | Path to your vault directory |
| `OPENCLAW_GATEWAY` | `http://127.0.0.1:18789` | OpenClaw gateway URL |
| `SBV_MODEL` | `maple/gpt-oss-120b` | LLM model for clustering and insights |
| `SBV_ATOMS_FILE` | `data/second-brain-atoms.json` | Output path for parsed atoms |
| `SBV_CLUSTERS_FILE` | `data/second-brain-clusters.json` | Output path for cluster data |
