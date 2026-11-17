# skill-clean-audit

> First-Principles Clean Code Auditor — a **read-only, readable, reusable** agent skill. Current version **v1.3.0**.
> 第一性原理 Clean Code 审计法 —— 一个**只读、可读、可复用**的 Agent Skill。当前版本 **v1.3.0**。

**Compliance / 合规**: purely local, read-only audit — no network, no credentials, no third-party APIs; provides / instructs / supports no means to circumvent network-management measures. See *Compliance & Boundary Statement* in SKILL.md.

From one root premise — **"code is written for humans"** — it derives two criteria and scores code red / amber / green, explicitly permitting *intentional, documented, scoped* tech debt to remain.

Built to audit your own **WorkBuddy / Claude / any-agent skill scripts** or other Python code, emitting an evidence-backed (`file:line`) checklist report. **This skill reads only, never edits** — fixes go to the next pass.

---

## Why it is not "yet another clean-code skill" / 为什么它不是「又一个 clean code skill」

Three families of related skills exist; this one occupies the gap none of them fills well:

| Red ocean | Representative | Our difference |
|---|---|---|
| App / PR code (correctness·security·perf) | code-review, review-pr, smart-code-review | Audits readability / maintainability only (comprehension & change risk), not correctness |
| Rule handbooks | clean-code (SRP/DRY/KISS) | Rules are *derived*, not dogmatic givens |
| Skill security | skill-vetting, agent-skills-audit | Audits only its own scripts' readability — zero network, zero credentials, read-only |

**Three differentiators / 三个差异化**: ① rules derived from first principles; ② two axes (cost vs risk), not category buckets; ③ permits intentional debt (amber tier).

---

## First-Principles Derivation / 第一性原理推导

1. **Root premise / 根前提**: code is written for humans. Machines only care whether syntax is valid, not naming / length / comments; code's real life is in the countless times it is read, modified, and maintained by another person (including future you).
2. From this, only two criteria follow / 由此只推出两根判据:
   - **A. Comprehension cost / 理解成本** — intent and boundaries obvious at a glance.
   - **B. Change risk / 修改风险** — a change doesn't quietly break something else.
3. Every concrete rule is a subtree of these two. Anything that fails "does it actually lower comprehension or change cost?" is noise.

> **Key reversal / 关键反推**: checklist-for-its-own-sake (splitting into tiny functions to be short, abstracting unused interfaces for DRY) raises cost — that is dirty.

---

## Severity (Red / Amber / Green) / 严重度（红 / 黄 / 绿）

- 🔴 **Red · dirty on sight, fix first / 红 · 出现即脏，优先修**: implicit `import *`, contradictory docs, comments degraded into a changelog, module-level mutable global controlling behavior, name≠behavior / hidden side effects (CQS violation), duplicated logic (DRY violation), bare `except` swallowing errors.
- 🟡 **Amber · intentional debt, needs comment + scope / 黄 · 有意的债，需注释 + 范围可控**: long functions (>40 lines but cohesive), unnamed magic numbers/strings, intentional best-effort `except`. Amber = temporarily acceptable, but the "why" must be written and the scope controlled.
- 🟢 **Green · clean on sight / 绿 · 出现即干净**: naming is documentation, explicit beats implicit, behavior depends only on inputs, tested, every `except` is precise.

Full interactive checklist: **[`assets/clean_code_checklist.en.html`](assets/clean_code_checklist.en.html)** (open in a browser to tick items, with a live counter). 中文版 / Chinese: **[`assets/clean_code_checklist.html`](assets/clean_code_checklist.html)**.

---

## Directory Layout / 目录结构

```
skill-clean-audit/
├── SKILL.md                       # methodology + audit flow + output format + boundaries + compliance + quick start + language
├── LICENSE                        # MIT (for open source; excluded from SkillHub / ClawHub publish packages)
├── README.md                      # Chinese README. NOTE: ClawHub publish package omits README.md
├── README.en.md                   # this file (English README)
├── CHANGELOG.md                   # version history
├── .gitignore                     # ignores generated audit artifacts
├── .clawhubignore                 # ClawHub exclusion manifest (incl. LICENSE + the dev export script, NOT metric_probe.py)
├── assets/
│   ├── clean_code_checklist.html  # interactive checklist (Chinese)
│   └── clean_code_checklist.en.html # interactive checklist (English)
├── references/
│   ├── clean_code_audit_sample.md # full sample (Chinese, synthetic functional aggregation)
│   ├── clean_code_audit_sample.en.md # full sample (English)
│   ├── clean_code_audit_sample_complex.md  # complex sample (Chinese: class/inheritance/async/global)
│   ├── clean_code_audit_sample_complex.en.md # complex sample (English)
│   ├── faq.md                     # FAQ (Chinese)
│   ├── faq.en.md                   # FAQ (English)
│   └── smells_crosswalk.md        # Uncle Bob smells → A/B axes + red/amber/green crosswalk
└── scripts/
    ├── metric_probe.py            # optional metric probe (pure stdlib, hints only)
    └── clean_code_clawhub_export.py # dev export script (excluded from ClawHub)
```

> **Bilingual / 双语**: every artifact (checklist, samples, FAQ, README) ships in both Chinese and English; pick the `auto`/`zh`/`en` mode via *Language Selection* before starting — language is never a hidden default.

### Which file to read / 我该读哪个文件

| When / 何时 | Read / 读 |
|---|---|
| Normal audit | `SKILL.md` *Audit Flow* · `assets/clean_code_checklist.html` (English `.en.html`) |
| Is this smell A or B? | `references/smells_crosswalk.md` |
| Full report example | `references/clean_code_audit_sample.md` (or `.en.md`) |
| Class / inheritance / async / global-state code | `references/clean_code_audit_sample_complex.md` (or `.en.md`) |
| Boundaries, artifact locations, exceptions, artifact mapping, metric definitions | `references/faq.md` (or `.en.md`) |
| Quick suspect scan | `scripts/metric_probe.py --src <file>` |

---

## Execution Model (Methodology, Not Tool) / 执行模型（方法论型，非工具型）

This skill ships criteria + flow + a tickable checklist that you (the agent) apply with `file:line` evidence. The core action is *judgment* — "does this code lean A or B, is it red or intentionally-amber debt" — which is human reasoning and cannot be pre-encoded into a deterministic pipeline.

**The absence of an end-to-end automation script is a design decision, not a gap.** The `scripts/metric_probe.py` shipped here is an *optional accelerator* — it locates suspects fast but *hints only, never grades*.

本 skill 交付「判据 + 流程 + 可勾选清单」，由你逐项判断并给 `文件:行号` 证据。审计的核心动作是**判断**，本质是人的推理，**无法预先写成确定性自动流程**。**没有端到端自动化脚本是设计决策，不是缺失**；`metric_probe.py` 仅为可选加速器（只提示不判级）。

---

## Usage / 用法

### In WorkBuddy / 在 WorkBuddy 里

Place the whole directory at `~/.workbuddy/skills/skill-clean-audit/`, then in chat say:

> "Audit `~/.workbuddy/skills/demo-skill/scripts/aggregate.py` with first principles"
> 「用第一性原理审一下 `~/.workbuddy/skills/demo-skill/scripts/aggregate.py`」

or any trigger / 或任一触发词: comprehension/change risk, clean code audit, audit my skill scripts, score code red/amber/green.

It copies `assets/clean_code_checklist.html` (Chinese) or `assets/clean_code_checklist.en.html` (English) into your workspace and writes the report to `<workspace>/clean_code_audit_<target>.md`.

> **Pick language / 选语言**: say `zh` to force Chinese, `en` to force English, or leave it for `auto` (follows your message). See *Language Selection* in SKILL.md.

### Porting the method to other platforms / 方法论迁移到其他平台

The *Boundary Statement* in SKILL.md names WorkBuddy's equivalent skills (e.g. `code-review-assistant`). The method is platform-agnostic — apply its two criteria + red/amber/green to any script on your platform; no rewrite needed.

---

## Boundaries vs Other Tools (avoid overlap) / 与其他工具的边界（避免重叠）

- ❌ Generic PR/MR review → use your platform's PR-review tool
- ❌ Code-style handbook → use clean-code (SRP/DRY/KISS)
- ❌ Lint / format → use project-code-standard (ruff/eslint/prettier)
- ✅ This skill only does **first-principles readability / maintainability audit**, and **reads only, never edits**

---

## License / 许可证

MIT © 2026

> **Multi-platform note / 多平台发布说明**: this repo (GitHub / SkillHub) is distributed under MIT; the ClawHub package defaults to **MIT-0** per platform policy (LICENSE excluded via `.clawhubignore`, `license` field stripped from frontmatter).
