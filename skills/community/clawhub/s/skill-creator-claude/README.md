# skill-creator-claude

[中文版](./README_CN.md)

> Anthropic's best-in-class skill creation methodology — now available on any agent platform.

Anthropic built an exceptional skill-creator into Claude Code: a full development loop covering drafting, eval, iteration, benchmarking, and description optimization. This repo is a minimal, faithful adaptation that removes Claude Code-specific dependencies so anyone can use it — no matter which agent platform they're on.

---

## Origin & Attribution

- **Original author**: Anthropic
- **License**: Apache 2.0 (see [LICENSE](./LICENSE))
- **Original source**: Claude Code built-in plugin (`~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator`)
- **Full experience**: [Claude Code](https://claude.ai/code) — free to use, and where 100% of the features work

This repository is a derivative work under Apache 2.0. All intellectual credit belongs to Anthropic.

---

## Our Philosophy

- **Minimal changes**: Only remove hard dependencies that prevent cross-platform use. The methodology, scripts, and tooling are untouched.
- **Full attribution**: All copyright notices and LICENSE files preserved as required by Apache 2.0, and as a matter of principle.
- **Accessible to everyone**: The original skill-creator is outstanding — it shouldn't be exclusive to Claude Code users.
- **Gateway, not replacement**: If you want 100% of the capability, use Claude Code. This version is the on-ramp.

---

## What Was Changed

Only **4 modifications** to `SKILL.md` (~10% of the file). Everything else is identical to the original.

| # | Change | Reason |
|---|---|---|
| 1 | Added modification notice comment at top of SKILL.md | Apache 2.0 requires noting changes in modified files |
| 2 | Description Optimization Step 3: added platform note that `run_loop.py` requires the `claude -p` CLI, with a manual fallback for other platforms | `claude -p` is a Claude Code-exclusive CLI tool |
| 3 | "Package and Present": removed the `present_files` tool condition, simplified to always run `package_skill.py` | `present_files` is a Claude Code-exclusive tool |
| 4 | Merged "Claude.ai-specific" and "Cowork-Specific" sections into a single "Platform Notes" section; removed TodoList reminder | Unified cross-platform guidance; removed Claude Code UI references |

**Unchanged** (i.e., everything that matters):
- Complete skill development methodology
- All Python scripts (`run_eval.py`, `run_loop.py`, `improve_description.py`, etc.)
- Eval viewer and benchmark system
- Grading and blind comparison workflows
- All agent files (`agents/grader.md`, `agents/comparator.md`, `agents/analyzer.md`)
- `references/schemas.md`

---

## Feature Comparison

| Feature | This version | Claude Code (original) |
|---|---|---|
| Skill drafting & iteration | ✅ | ✅ |
| Eval runner & viewer | ✅ (requires Python) | ✅ |
| Benchmark comparison | ✅ (requires subagents) | ✅ |
| Description improvement loop | ✅ (requires `ANTHROPIC_API_KEY`) | ✅ |
| Description trigger-rate testing | ❌ requires `claude -p` CLI | ✅ |
| Skill packaging (`.skill` file) | ✅ | ✅ |

---

## Installation

### Via ClawHub
```bash
clawhub install plabzzxx/skill-creator-claude
```

### Manual
Clone or copy this entire repository into your agent platform's skills directory.

### Optional: description improvement script
`improve_description.py` uses the Anthropic API directly and works on any platform:
```bash
export ANTHROPIC_API_KEY=your_key_here
```

---

## Credits

All design, code, and methodology copyright Anthropic, licensed under Apache 2.0.  
If this skill is useful to you, go try [Claude Code](https://claude.ai/code) — that's where the full picture lives.
