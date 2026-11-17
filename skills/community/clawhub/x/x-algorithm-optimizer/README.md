<div align="center">

# X Algorithm Optimizer

**An Agent Skill that writes tweets with knowledge reverse-engineered from X's
open-source ranking code.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/type-Agent%20Skill-8A2BE2.svg)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
[![GitHub stars](https://img.shields.io/github/stars/zfoong/X-algorithm-optimizer?style=social)](https://github.com/zfoong/X-algorithm-optimizer/stargazers)
[![Based on](https://img.shields.io/badge/grounded%20in-X%20open--source%20algorithm-000000.svg)](https://github.com/twitter/the-algorithm)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

<sub>Every claim traces to a specific line of X's published algorithm.</sub>

</div>

---

Most advice about "growing on X" is folklore. In August 2026, X open-sourced the
code that actually ranks the For You feed. This skill reads that code so your
agent can write posts optimized for how the algorithm *really* scores and
distributes them, and can tell you exactly which mechanism each recommendation
comes from.

## 🔑 The whole secret in one table

X scores a post as a weighted sum of the actions it predicts a viewer will take.
The weights are wildly asymmetric, and that asymmetry is the entire game:

| A viewer... | is worth | takeaway |
|---|---:|---|
| copies your link to share it | **+20.0** | forwarding beats everything |
| replies / quotes / DMs it to a friend | **+5.0** | conversation and sharing |
| follows you from the post | **+4.0** | |
| **likes it** | **+0.5** | likes are nearly worthless |
| taps "not interested" | **−43.2** | |
| mutes you | **−58.8** | |
| **reports it** | **−234.0** | one report cancels ~468 likes |

A post whose negatives outweigh its positives does not just rank low. It
collapses to near zero and sinks. So the two laws are: **optimize for "send to a
friend," not "like,"** and **avoiding negative signals beats chasing positive
ones.** The rest of the skill is the detail behind those two sentences.

## 🧠 What it does

Point your agent at this skill and ask it to write or review a post. It reads
X's published ranking code and drafts or critiques your post against the real
scoring weights, retrieval paths, and suppression rules, runs a negative-signal
audit, and explains the exact mechanism behind every suggestion. The result is
posts optimized for how the For You feed actually distributes content.

## 📦 Install

The skill is plain Markdown plus one optional, dependency-free Python script, so
it works with any AI agent that can read files in your project. Clone it once:

```bash
git clone https://github.com/zfoong/X-algorithm-optimizer
```

Then wire it into your agent:

- **Claude Code:** clone (or symlink) it straight into your skills directory and
  it loads automatically:
  ```bash
  git clone https://github.com/zfoong/X-algorithm-optimizer \
    ~/.claude/skills/x-algorithm-optimizer
  ```
- **OpenAI Codex:** keep the folder in your repo and reference `SKILL.md` from
  your `AGENTS.md`, or open a session with "read `x-algorithm-optimizer/SKILL.md`
  and follow it."
- **Cursor:** add the folder to your workspace and point the agent at it with
  `@SKILL.md`, or register it as a project rule.

For any other assistant (Gemini CLI, GitHub Copilot, and the like), just have it
read `SKILL.md`. That file is the entry point, and the agent pulls in the
`references/` files only as a task needs them.

## 🚀 Usage

Once your agent can see `SKILL.md`, just ask for post help. In Claude Code it
activates automatically; with other agents, name the skill or your posting task
and it pulls in the right references. Try:

```text
Write a tweet about my open-source side project. I have ~800 followers.
```
```text
Review this draft before I post it: "<your draft>"
```
```text
Why isn't my post getting any reach beyond my followers?
```
```text
Give me a reply-optimized and a forward-optimized version of this post.
```

The agent will pull the exact weights and thresholds from the reference files,
draft or critique against them, run a negative-signal audit, and explain the
mechanism behind each suggestion.

## 🔍 The post critic

A dependency-free heuristic scorer you can also run standalone. It estimates
which actions your wording invites, scores the draft with the real weight table,
and flags risks.

```bash
python scripts/post_critic.py "your draft post here"

# compare two variants and pick the stronger one
python scripts/post_critic.py --compare "draft A" "draft B"
```

```text
============================================================
X POST CRITIC - heuristic reach score (directional, not a model)
============================================================

Estimated weighted score: +0.081  [############------------]
Verdict: ok

Flags:
  - [+] Forward-worthy framing detected. Targets the 20x copy-link share. Good.
  - [+] Question present. Targets reply weight (5.0). Good.
```

It is a writing aid, not a simulator of X's ML model (which never sees your raw
text). Treat the score as directional.

## 📂 What's inside

```
x-algorithm-optimizer/
├── SKILL.md                        the agent's playbook (the 5-step workflow)
├── references/
│   ├── scoring-weights.md          weight table, score math, offset transform
│   ├── distribution-mechanics.md   what the model sees, retrieval, cold-start, DPP
│   ├── negative-signals.md         filters, labels, the OON-only "shadowban" set
│   ├── account-playbooks.md        strategy by account size and content format
│   ├── examples.md                 worked weak-to-strong post rewrites
│   └── myths.md                    popular advice the ranking code refutes
├── scripts/
│   └── post_critic.py              offline heuristic scorer (stdlib only, --compare)
├── CONTRIBUTING.md
├── LICENSE                         MIT
└── README.md
```

`SKILL.md` is the entry point the agent loads. The `references/` files are
progressive detail it pulls in only when a task needs them, which keeps the
core playbook small.

## ⚙️ How it works

The skill encodes four principles from the code:

1. **The weight table is the value system.** Optimize for the high-weight
   actions (forwarding, replies, follows), not the low-weight one (likes).
2. **Negative signals dominate.** A single report or a spike in
   blocks-relative-to-likes can collapse a post or apply an account-level label
   that silently caps stranger-reach. Avoiding harm outranks chasing reach.
3. **Reach is retrieval.** Strangers only see you if your content's embedding
   sits near what they engage with, so niche consistency and early engagement
   from a coherent audience are the real out-of-network levers.
4. **Cite the mechanism.** Every recommendation names the file and value it
   comes from, so advice is auditable and survives the algorithm changing.

## 🎯 Accuracy and versioning

Grounded in the **August 2026 snapshot** of X's open-source algorithm. The
scoring weights are production-synced defaults that X periodically rewrites via
cron, so exact decimals drift over time. The *structure* (what is rewarded, what
is suppressed, how distribution works) is far more stable than the numbers. To
refresh values, re-derive them from a fresh clone of the algorithm repo,
starting with `home-mixer/params/param.rs`.

This is an independent analysis of public code. It is not affiliated with,
endorsed by, or an official product of X.

## 🤝 Contributing

Contributions are welcome: refreshed weights after an upstream change, new myths
with citations, additional worked examples, or critic improvements. See
[CONTRIBUTING.md](CONTRIBUTING.md). The one hard rule: every factual claim must
cite the specific file or value in X's algorithm it comes from.

## ⚖️ Scope and ethics

This skill optimizes **genuine, policy-compliant content** for legitimate reach.
It does **not** assist with spam or engagement farming, coordinated inauthentic
behavior, fake or bought engagement, ban evasion, or evading safety labels on
content that genuinely violates policy. The suppression mechanics are documented
so honest creators avoid accidental throttling. The most durable way to win this
algorithm is to make content people genuinely want to forward.

## 📜 License and attribution

Released under the [MIT License](LICENSE).

The skill is an independent work: original documentation, analysis, and code.
The factual claims are derived from reading X's
[open-source algorithm](https://github.com/twitter/the-algorithm), which is
published under Apache-2.0. Facts and mechanisms are not themselves
copyrightable; this repository contains none of X's source code.
