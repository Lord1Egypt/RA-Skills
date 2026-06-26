<p align="center">
  <img src="assets/brand.png" width="360" alt="TaijiOS · Kongming × Bagua × Evolving Brain">
</p>

# 🎴 Zhuge · AI Prediction Advisor (`zhuge-skill`)

> **Stop burning tokens on every decision.** Do 90% of structured reasoning on CPU; call the LLM only when you actually need its creativity.
>
> Integrates **API-Football / The Odds API / Understat xG** across 5 data sources · **6-yao scoring + 64-hexagram decision tree** · experience self-learning · works with **DeepSeek / Kimi / Qwen / ZhipuAI / Claude / GPT / Gemini** (12 providers, pick any).

[中文 README](README.md) · **English**

<p align="center">
  <img src="assets/demo.png" width="720" alt="Zhuge Skill · Reasoning demo">
</p>

<p align="center">
  <em>One sentence <code>predict "Napoli vs Lazio"</code> → 5-source fusion → 6-dimension yao scoring → 64-hexagram decision.</em>
</p>

---

## ⚡ Why cheaper than a pure LLM agent

Most LLM agents spend **3,000 - 10,000 tokens per decision**, with ~80% going to "re-feeding context so the model can reconfirm the rules". Zhuge splits this into two halves:

| Path | Token cost | Notes |
|---|---|---|
| Pure LLM agent decision | **~3,000-10,000 / decision** | Whole context goes into the prompt each time |
| Zhuge: data → yao scoring → hexagram → decision | **0 tokens** | Pure CPU numerical reasoning |
| Zhuge: hit a cached crystal | **0 tokens** | Reuse a proven structured pattern, skip the LLM |
| Zhuge: let LLM polish the Kongming commentary (optional) | **~200-500 tokens** | Only when you explicitly ask for it; toggleable |

**Real workload — batch predicting 50 matches:**

- Pure LLM agent: ~250,000 tokens (¥15-50 / US$2-7 depending on model)
- Zhuge (no LLM calls): **~0 tokens / ¥0**
- Zhuge (LLM commentary per match): ~15,000 tokens (¥1-3 / US$0.15-0.5)

This is the core value — **not because the *I Ching* is magic, but because work structured reasoning can do should not cost LLM tokens**.

---

## 🚀 30-second quick start

```bash
# 1. Clone
git clone https://github.com/yangfei222666-9/zhuge-skill.git
cd zhuge-skill

# 2. One-click launch (welcome animation + guided setup)
python start.py
```

That's it. `start.py` auto-runs:

- Cyber-Zhuge welcome animation
- Python / deps / API-key sanity check
- Interactive wizard (optional — or just `python start.py demo`)
- First prediction

### Or zero-config demo

```bash
python start.py demo
# runs with bundled sample data — no API keys needed
```

---

## 🎮 Host compatibility

| Host | Install path |
|------|--------------|
| Claude Code | `~/.claude/skills/zhuge-skill/` |
| Cursor | `.cursor/rules/zhuge.mdc` (project rule) |
| OpenClaw | `~/.openclaw/skills/zhuge-skill/` |
| Hermes Agent | `~/.hermes/skills/zhuge/` |
| Plain Python | just `python start.py` |

Each host has a copy-pasteable snippet in [README.md §全平台兼容](README.md#-全平台兼容) (Chinese README, but the snippets themselves are shell commands / JSON / mdc — readable as-is).

---

## 🧠 Architecture (one screen)

```
match input  →  5-source fetch (API-Football / The Odds / Understat / H2H / cross-check)
             →  6-dimension yao scoring (attack/defense/morale/injury/home-away/h2h/odds)
             →  64-hexagram recognition (yin/yang per dimension → hexagram index)
             →  decision engine (1X2 + over/under + confidence)
             →  [optional] crystal match — if history says this pattern hit X%, weight it
             →  [optional] LLM commentary — Kongming-style prose, only if requested
```

Data / results:

- `data/experience.jsonl` — your prediction history (local only)
- `data/crystals_local.jsonl` — distilled patterns (schema v2: `first_seen` / `last_seen` / `recurrence_count` for tracking which patterns actually get reused)
- `data/crystals_shared.jsonl` — anonymous patterns pulled from the public pool (read-only; see [PRIVACY.md](PRIVACY.md))

---

## 🔐 Privacy (architectural, not a promise)

Starting from v1.0.1, `scripts/sync.py` has **only `pull` and `status` subcommands** — there is literally no code path that uploads your local data anywhere. This isn't "off by default", it's **not written at all**. See [PRIVACY.md](PRIVACY.md) for the full contract and the 4-line audit script you can run in 2 minutes.

The only outbound calls are:

- `sync.py pull` → HTTP GET from a public GitHub URL (read-only, no body)
- `backfill.py` → data-source APIs for match results (team names / match dates only)
- LLM commentary → whichever LLM provider you configured (prompt only, no local DB)

No telemetry. No analytics. No "anonymous diagnostics".

---

## 📜 License

MIT. Use it, fork it, ship it.

---

## 🌍 Part of TaijiOS

`zhuge-skill` is the first public skill out of [**TaijiOS**](https://github.com/yangfei222666-9/TaijiOS) — a self-learning AI operating system with 5 I-Ching-bound engines, a 346-heartbeat Ising physics experiment, and 12-provider LLM gateway. If the token-saving structure here resonates, check the parent project.

---

## 📬 Feedback / Contact

Tried it? Couldn't install it? Have ideas? **Reach out directly** — this is a very early project and every piece of feedback (even "it crashed on my machine") gets read.

- **Email (preferred)**: `yangfei222666@gmail.com`
- WeChat (secondary, Chinese-speakers): `yf529486`
- GitHub Issue: [open one](https://github.com/yangfei222666-9/zhuge-skill/issues/new)

---

<sub>README auto-generated + human-curated · numbers in this doc (3,000-10,000 tokens, 5 sources, 64 hexagrams, 12 providers) match the actual code & config. `grep` freely.</sub>
