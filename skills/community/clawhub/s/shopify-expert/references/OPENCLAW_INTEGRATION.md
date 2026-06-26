# OpenClaw integration

## Skill entry

- Install as **`shopify-expert`** (folder or ClawHub slug aligned with `metadata.openclaw.skillKey`).
- Configure env under `skills.entries["shopify-expert"].env` or host environment — see [AUTH.md](AUTH.md).

## Tools

- At minimum, allow **`curl`** if the agent should call Shopify HTTP APIs.
- Other tools (`exec`, browser, file edits) are **optional** and must match your trust and sandbox policy.

## Official OpenClaw docs

- [Skills](https://docs.openclaw.ai/tools/skills)
- [Agent tools](https://docs.openclaw.ai/plugins/agent-tools)
