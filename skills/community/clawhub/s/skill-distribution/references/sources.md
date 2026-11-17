# Sources and what was not verified

Checked 2026-10-10.

## Read directly (primary docs)

- Agent Skills specification — https://agentskills.io/specification
- skills CLI — https://github.com/vercel-labs/skills · https://skills.sh/docs
- agentskill.sh submission — https://agentskill.sh/submit
- ClawHub — https://docs.openclaw.ai/clawhub · https://docs.openclaw.ai/clawhub/skill-format
- Claude Code plugins — https://code.claude.com/docs/en/plugins/publish · https://code.claude.com/docs/en/plugins/create-marketplace
- OpenAI plugins and skills — https://developers.openai.com/plugins/build/plugins · https://learn.chatgpt.com/docs/build-skills
- Agensi — https://www.agensi.io/ · SkillHQ — https://skillhq.dev/ · MCP Market — https://mcpmarket.com/sell

## Seen first-hand while publishing

- ClawHub login is device-code only; the browser-callback flow shows "CLI login has moved" (2026-10-10).
- `claude plugin validate --strict` is rejected as an unknown option by Claude Code 2.1.132.
- The skills CLI 1.7.2 needs Node 22.20 or newer.

## From search results or secondary guides only

- OpenAI submission prerequisites (identity verification, `api.apps.write`); the "Submit plugins" page returned 404.
- claude.ai zip upload menu names and the 50 MB limit.
- Hermes `skills publish` and `skills tap add` commands.
- Gemini CLI extension publishing details.
- How skills.sh decides "Official" and what its audits check.

## Not checked at all

- Trademark or naming rules on any registry.
- Whether Dots, Muse or Grok load SKILL.md skills.
- Cursor, Windsurf and other editor-specific stores beyond what the skills CLI installs into.
