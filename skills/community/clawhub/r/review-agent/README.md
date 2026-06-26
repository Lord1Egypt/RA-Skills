# Review Agent (review-agent)

Pre-meeting review coach for Lark/Feishu (or WeCom). 1942 US Army Completed Staff Work.

## Install

```bash
clawhub install review-agent --force
# finish setup:
git clone https://github.com/jimmyag2026-prog/review-agent-skill ~/code/review-agent-skill
cd ~/code/review-agent-skill && bash install.sh --enable-only
```

⚠ **Use v2.1.2 or later** — v2.0-v2.1.1 had install-time bugs (wrong feishu key / macOS-only monitor.js path / unexpanded tilde). v2.1.2 patchers auto-recover broken installs.

## Channel support

feishu / wecom only for per-peer subagent. Others → shared main agent.

See https://github.com/jimmyag2026-prog/review-agent-skill
