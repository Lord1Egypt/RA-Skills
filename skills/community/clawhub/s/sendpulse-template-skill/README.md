# SendPulse Email Template Skill — v1.0

An AI skill that generates production-ready, responsive **HTML email templates** for the SendPulse
builder, and guides uploading them via the SendPulse **MCP server** or **API**. Works for any brand,
any language, and serves both beginners and expert marketers.

It's a plain folder — `SKILL.md` (instructions) + `references/` (on-demand docs) + `assets/examples/`
(sample templates). No installation, no dependencies — just make it available to your AI assistant.

---

## Install

### Claude Code (CLI / IDE extension)
- **Personal (all projects):** copy the `sendpulse-template-skill/` folder into
  - macOS/Linux: `~/.claude/skills/`
  - Windows: `%USERPROFILE%\.claude\skills\`
- **One project / team (commit to repo):** copy it into `.claude/skills/` in the project.
- The folder name must stay `sendpulse-template-skill`. It loads automatically — just ask the
  assistant to "create an email template for …" and the skill triggers.

### Claude.ai / Claude Desktop
- Zip the `sendpulse-template-skill/` folder.
- Settings → **Capabilities → Skills** → **Upload skill** → choose the zip. Enable it.
- Start a chat and ask to build an email — it triggers on the description.

### Cursor
- Add the `sendpulse-template-skill/` folder to your project.
- Create a project rule (e.g. `.cursor/rules/sendpulse-email.md` or an `AGENTS.md`) with:
  *"When asked to create a SendPulse email/HTML template, follow
  `sendpulse-template-skill/SKILL.md` and the files it links in `references/`."*
- Then ask Cursor to create the email.

### ChatGPT
- **Custom GPT (best):** create a GPT, upload `SKILL.md` + the `references/*.md` files as **Knowledge**,
  and put in the instructions: *"Follow SKILL.md and its references to generate SendPulse email
  templates."*
- **Plain chat:** paste the contents of `SKILL.md` (and the relevant `references/*.md`) into the chat,
  then describe the email you want.

### Other LLMs / agents
- The skill is just Markdown + HTML with no tool dependencies. Provide `SKILL.md` (and references) as
  system prompt / context / knowledge files. The assistant follows them the same way.

---

## Connect SendPulse (optional, for auto-upload)
To let the assistant upload templates and manage mailings without copy-paste, connect the SendPulse
**MCP server** in your tool's MCP/connector settings:
- Server URL: `https://mcp.sendpulse.com/mcp`
- Authenticate with a SendPulse **Single API Key** (Settings → API → API keys).
- See `references/sendpulse-mcp.md` (MCP) and `references/sendpulse-api.md` (REST API) for details.

Without a connection, the skill still produces HTML you paste into the SendPulse HTML editor.

---

## Use
Just describe what you need: *"Make a promo email for our spring sale, brand color #0055CC."*
The skill detects the email type, asks only what's missing, and returns a ready HTML fragment plus
subject-line options. See `CHANGELOG.md` for version history.
