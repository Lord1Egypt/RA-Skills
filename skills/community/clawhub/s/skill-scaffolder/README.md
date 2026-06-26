# skill-scaffolder

A Claude Code skill that **scaffolds new skills** with SkillReducer structural constraints pre-applied. Produces a compression-ready `SKILL.md` on day 0, so you don't need to `skill-compressor` it on day N.

> **中文简介**：从 idea 一次性生成结构精简的 Claude Code skill 骨架。基于 [SkillReducer](https://arxiv.org/abs/2603.29919) 论文把"结构约束"前置到创作阶段——不是"写完再 eval 再改"，而是"从一开始就不能写错"。和 [`skill-compressor`](https://github.com/David0Ming/skill-compressor) 配套使用：一个搭新的，一个压老的。

## Why

Official `skill-creator` optimizes writing quality via the **write → test → eval → iterate** loop. But the SkillReducer paper (55,315-skill empirical study) identifies three problem classes that **eval metrics can't catch**:

- **26.4%** of skills have missing / short descriptions — the router never matches, test queries all miss, eval gives no signal
- Only **38.5%** of body content is actionable core rule; eval pass rate ≠ structural health
- **10.7%** of skills should retire — but `skill-creator` assumes a skill *should* exist

**Conclusion**: structural problems must be locked down *before* creation via hard constraints, not after via eval.

## What it does

Takes a skill idea and a target path, produces a full scaffold:

```
<path>/<skill-name>/
├── SKILL.md                 # core_rule only, ≤ 300 body tokens
├── background.md            # (if any) — why / rationale, with when:/topics:
├── examples.md              # (if any) — I/O demos, with when:/topics:
├── templates.md             # (if any) — boilerplate, with when:/topics:
└── ARCHITECT_REPORT.md      # Gate-0 result, taxonomy distribution, Faithfulness audit
```

Each split file ships with `when:` + `topics:` frontmatter for progressive disclosure.

## The 7 steps (one-shot, not guided)

| Step | Name | Output |
|------|------|--------|
| 0 | **Retirement check (Gate 0)** | 3 trigger scenarios + recommendation (build / retire) |
| 1 | **Routing signal 3-elements** | primary capability + trigger condition + unique identifier (10–20 tok each) |
| 2 | **Description draft** | ≤ 120 tok description + DDMIN self-check |
| 3 | **Body taxonomy pre-labeling** | every rule tagged `core_rule` / `background` / `example` / `template` / `redundant` |
| 4 | **File split layout** | `SKILL.md` keeps core_rule only; split files get `when:` + `topics:`; < 50-tok files merge back |
| 5 | **Four anti-pattern checks** | no examples-as-spec / no thresholds in background / no trigger-keyword dumps / no redundant refs |
| 6 | **Faithfulness self-audit (Gate 1)** | every operational concept lives in core_rule ∪ split files |
| 7 | **Output** | scaffold + `ARCHITECT_REPORT.md` |

## Pipeline position

```
      ┌── skill-scaffolder ──┐                    ┌── skill-compressor ──┐
idea →│  day-0 pre-compress  │ → SKILL.md → (...) │  day-N post-bloat    │ → SKILL.md
      └──────────────────────┘                    └──────────────────────┘
```

**Theoretical guarantee**: output of `skill-scaffolder` should be nearly un-compressible by `skill-compressor` — born compact. This is also the validation metric for scaffolder itself.

## Install

### Manual

```bash
git clone https://github.com/David0Ming/skill-scaffolder.git ~/.claude/skills/skill-scaffolder
```

### Via skills.sh

```bash
npx skills add David0Ming/skill-scaffolder
```

### Via ClawHub

```bash
clawhub install skill-scaffolder
```

## Usage

In any Claude Code session:

- `/skill-scaffolder`
- or: *"scaffold a skill that does X"*
- or: *"help me draft a new skill for Y"*

Claude walks the 7 steps in one shot and writes the scaffold to your chosen path.

## When NOT to use

- **Improving an old skill** → use [`skill-compressor`](https://github.com/David0Ming/skill-compressor)
- **Want guided iterative creation + eval loops** → use official `skill-creator`
- **Only 1–2 rules needed** → put them in `CLAUDE.md`, not a skill

## Credits

Methodology from: Chen et al., *SkillReducer: A Two-Stage Compression Method for Agent Skills*, [arXiv:2603.29919](https://arxiv.org/abs/2603.29919), 2026.

## License

Apache-2.0 — see [LICENSE](./LICENSE).
