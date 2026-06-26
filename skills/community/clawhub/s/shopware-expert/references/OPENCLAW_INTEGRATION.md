# OpenClaw: tools, sandbox, and this skill

How **OpenClaw** loads **skills**, applies **tool allowlists**, and interacts with **sandbox** policies, aligned with skill **shopware-expert**. If your OpenClaw version differs, follow the official docs.

## Official documentation (entry)

- [Tools and Plugins](https://docs.openclaw.ai/tools)
- [Skills](https://docs.openclaw.ai/tools/skills)
- [Skills config](https://docs.openclaw.ai/tools/skills-config): `skills.entries`, `env`, sandbox notes
- [Creating skills](https://docs.openclaw.ai/tools/creating-skills)
- [Sandbox vs Tool Policy vs Elevated](https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated)

## Global tool policy

- **`tools.deny` wins** over allow.
- **`tools.profile`** may shrink the baseline allowlist; per-agent overrides still apply.
- **`group:openclaw`** covers **built-in** tools only, not arbitrary external plugins. If you add a Shopware-specific plugin later, list its tools **explicitly** in `tools.allow` and, if needed, in **`tools.sandbox.tools.allow`**.

## Sandbox

Sandboxed sessions may block `exec`, HTTP, or custom tools even when global `tools.allow` includes them. On messages like "blocked by sandbox tool policy", adjust **`tools.sandbox.tools.allow`** per OpenClaw documentation.

Diagnostics (examples):

```bash
openclaw sandbox explain
openclaw skills list --eligible
```

## Secrets injection

- `skills.entries["shopware-expert"].env` merges into the **host** process for eligible runs.
- Keep secrets out of prompts and logs; prefer env-backed configuration.

## Skill metadata

- **`metadata.openclaw.requires`** in `SKILL.md` gates eligibility (bins, env vars). Keep it aligned with [AUTH.md](AUTH.md) and `.env.example`.
