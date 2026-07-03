# token-slim

> Guided token optimization for AI agent workspaces — works on OpenClaw, Claude
> Code, and any agent runtime with a writable working directory.

Every project-context file (memory index, agent config, heartbeat, etc.) gets
injected into **every single session**. Keeping them lean = direct, compounding
token savings. token-slim audits your workspace, scores findings, and walks
you through targeted cleanup.

## What it does

- 📊 **Scan** — finds bloat in `MEMORY.md`, `AGENTS.md`, `memory/`, `memoryres/`
  and surfaces a prioritised list of optimisation opportunities
- 🎯 **Precise counting** — uses [tiktoken](https://github.com/openai/tiktoken)
  (`cl100k_base`) when available, falls back to a CJK-aware heuristic
- 🔥 **Brutal mode** — optional agent-config toggle that strips narration from
  responses for max output efficiency
- 🛡️ **Dry-run safe** — preview every change before touching files; auto-backup
  helper for the agent before any modification

## Install

### Via [clawhub](https://clawhub.com)
```bash
clawhub install token-slim
```

### Via [skills.sh](https://skills.sh)
```bash
npx skills install token-slim
```

### Manual
```bash
git clone https://github.com/Songhonglei/better-agent-skills.git
cp -r better-agent-skills/skills/token-slim ~/.claude/skills/
# or wherever your agent reads skills from
```

## Quick start

From the workspace root you want to scan:

```bash
# 1. (Optional) install tiktoken for precise counting
python3 <skill-install-path>/scripts/install_tiktoken.py --workspace .

# 2. Run a dry-run scan
python3 <skill-install-path>/scripts/scan_workspace.py --workspace . --dry-run
```

Or just say to your agent: **"save tokens"** / **"帮我省 Token"** — it will
pick up the skill, read the right reference file, and walk you through cleanup.

## Trigger phrases (English / 中文)

- "save tokens", "optimize tokens", "scan my workspace"
- "context window too large", "memory files too big", "trim workspace"
- "scan again", "find more savings", "what else can I optimize"
- "enable brutal mode", "disable brutal mode"
- 「帮我省 Token」「优化 Token 使用」「上下文太长了」「再扫一下」
- 「还有哪里可以优化」「开启狂暴模式」「关闭狂暴模式」

## tiktoken installation

The installer tries multiple sources with automatic fallback:

| Step | Source | Notes |
|------|--------|-------|
| 1 | PyPI official (pypi.org) | 2 retries |
| 2 | Tsinghua mirror | China-region acceleration |
| 3 | Aliyun mirror | China-region acceleration |
| 4 | Heuristic fallback | CJK/ASCII split, ~40-60% error |

The BPE vocabulary (`cl100k_base.tiktoken`, ~1.7 MB) is fetched automatically
by tiktoken on first encode from OpenAI's public blob and cached under
`<workspace>/.cache/tiktoken/` — **CWD-anchored** so it survives `$HOME` wipes
on container/VM environments where only the working directory is persistent.

Override the cache path with `TIKTOKEN_CACHE_DIR=/some/path` if you need to.

## Files

```
token-slim/
├── SKILL.md                          # Skill manifest (read by agents)
├── README.md                         # This file
├── LICENSE                           # MIT
├── scripts/
│   ├── scan_workspace.py             # Scanner — supports --dry-run / --json
│   └── install_tiktoken.py           # Multi-source tiktoken installer
└── references/
    ├── strategies.md                 # 7 strategies + scoring rubric
    ├── mode-a-onboarding.md          # First-time setup workflow
    └── mode-b-rescan.md              # On-demand re-scan workflow
```

## Requirements

- Python 3.8+
- Optional: `tiktoken` (install via bundled installer above)

## License

MIT — see [LICENSE](./LICENSE).

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
