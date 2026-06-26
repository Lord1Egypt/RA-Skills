# skill-compressor

A Claude Code skill that compresses other skills to cut token cost, based on the [SkillReducer](https://arxiv.org/abs/2603.29919) methodology — empirically validated on 55,315 public skills.

> **中文简介**：这是一个压缩 Claude Code skill 体积、降低 token 成本的 skill。输入任意 `SKILL.md` 路径，输出 `<skill>/.reduced/` 目录（含压缩版 `SKILL.md`、按类型拆分的 `background.md` / `examples.md` / `templates.md`，以及 `REDUCTION_REPORT.md`）。论文 600-skill 对照评估中，压缩后质量**反升 2.8%**——冗余内容会分散 agent 注意力。

## Why

Community skills have systemic bloat:

- **26.4%** have missing or under-length descriptions — the router never matches them, tokens burn in the candidate pool for nothing
- Only **38.5%** of body content is actionable core rule; 60%+ is background / example / template
- **14.8%** carry reference files that inject tens of thousands of tokens per invocation (100 SkillHub skills totaled 1.67M tokens)

Controlled evaluation on 600 skills found compressed versions **outperformed originals by 2.8%**. Non-essential content distracts the agent into searching for answers in irrelevant examples and background.

## What it does

Given a `SKILL.md` path, produces `<skill>/.reduced/` containing:

- Compressed `SKILL.md` (optimized description + core_rule-only body)
- Type-split `background.md` / `examples.md` / `templates.md`, each with `when:` and `topics:` frontmatter for progressive disclosure
- `REDUCTION_REPORT.md` with token deltas, classification distribution, and Faithfulness gate results

**The original file is never overwritten.** Output lands in `.reduced/`; you diff and replace manually.

## Method

Two stages plus two gates:

1. **Stage 1 — Description compression.** Use delta debugging (DDMIN) to reduce the description to 1-minimal: the shortest form that still uniquely routes.
2. **Stage 2 — Body classification.** Label each paragraph / bullet / code block against the 5-class taxonomy below; split into appropriate files.
3. **Gate 1 — Faithfulness (mandatory).** For every operational concept in the original body (verb, threshold, path, API name, env var), verify it still exists in the compressed core ∪ split files. Lost concepts trigger a type-level rollback; at most 2 rounds. Anything still missing stays in the original and is flagged "non-compressible" in the report.
4. **Gate 2 — Task evaluation (optional).** If test cases exist, run compressed vs. original; otherwise report "runtime behavior unverified."

### Five-class taxonomy

| Type | Definition | Destination |
|------|-----------|-------------|
| `core_rule` | Actionable directives (when / must / steps / prohibitions / numeric thresholds) | `SKILL.md` (always loaded) |
| `background` | Motivation, rationale, "why" explanations | `background.md` |
| `example` | I/O pairs, demonstrations, few-shot samples | `examples.md` |
| `template` | Paste-ready boilerplate, fixed formats, config snippets | `templates.md` |
| `redundant` | Duplicates or already covered in referenced files | Discarded |

### Typical result

From the paper's `marketing-strategy-pmm` walkthrough:

- Core-only invocation: 12,019 → 540 tokens (**−96%**)
- Full load with all references: 12,019 → 7,231 tokens (−40%)
- Gate 2 score: `score_C` (compressed) = 1.0 vs. `score_A` (original) = 0.93

## Install

### Manual (recommended)

```bash
git clone https://github.com/David0Ming/skill-compressor.git ~/.claude/skills/skill-compressor
```

Or symlink from a working directory you already clone into:

```bash
ln -s /path/to/skill-compressor ~/.claude/skills/skill-compressor
```

### Via skills.sh

```bash
npx skills add David0Ming/skill-compressor
```

### Via ClawHub

```bash
clawhub install skill-compressor
```

## Usage

Once installed, in any Claude Code session:

- `/skill-compressor`
- or: *"compress `~/.claude/skills/foo/SKILL.md`"*
- or: *"this skill is huge, token cost is exploding — slim it down"*

Claude walks the 8-step procedure and writes results to `<skill>/.reduced/`.

## Constraints (enforced by the skill)

- **Never overwrite** the original `SKILL.md`
- **Never drop** numbers, thresholds, paths, API names, env vars
- **Never modify** the frontmatter `name`
- **Never introduce** rules not present in the original skill
- **Never merge** across skills
- If a concept is still missing after 2 rollback rounds → preserve the original paragraph and mark "non-compressible" in the report

## When not to compress

- Skill is < 300 tokens (return < overhead)
- Body is already ≥ 80% `core_rule` (already optimized)
- Pure-template skill (no classification structure to exploit)

## Credits

Methodology from: Chen et al., *SkillReducer: A Two-Stage Compression Method for Agent Skills*, arXiv:2603.29919, 2026.

## License

Apache-2.0 — see [LICENSE](./LICENSE).
