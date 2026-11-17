# Plugins and app stores: Claude, ChatGPT/Codex, Gemini

The SKILL.md does not change. Each store needs a small manifest around the same `skills/` folder.

## Claude Code: your own plugin marketplace (no review)

Two files in the repo make it both a plugin and a marketplace.

`.claude-plugin/plugin.json`
```json
{
  "name": "my-skills",
  "displayName": "My Skills",
  "description": "What the skills do, in one line",
  "author": { "name": "Your Name" },
  "homepage": "https://github.com/owner/my-skills",
  "repository": "https://github.com/owner/my-skills"
}
```

`.claude-plugin/marketplace.json`
```json
{
  "name": "my-marketplace",
  "description": "What this marketplace offers",
  "owner": { "name": "Your Name" },
  "plugins": [
    { "name": "my-skills", "source": "./" }
  ]
}
```

- The entry `name` in `marketplace.json` must equal the `name` in `plugin.json`.
- Skills in `skills/<name>/SKILL.md` are picked up automatically and invoked as `/my-skills:<name>`.
- The plugin name is permanent: users install by `name@marketplace`, so renaming breaks every install. Change `displayName` instead.
- Versioning: bump `version` on every release, or leave it out so the commit SHA is used. A pushed change with an unchanged `version` never reaches users.
- Validate before pushing: `claude plugin validate --strict .` (older CLI versions do not know `--strict`; if it is rejected as an unknown option, run `claude plugin validate .`). Add a `description` to `marketplace.json` too, or validation warns.
- Test the real path: `claude plugin marketplace add ./` then `claude plugin install my-skills@my-marketplace`.

What to tell users:
```bash
claude plugin marketplace add owner/my-skills
claude plugin install my-skills@my-marketplace
```
A private repo is a private marketplace. Auto-update is off by default for third-party marketplaces.

Docs: https://code.claude.com/docs/en/plugins/publish · https://code.claude.com/docs/en/plugins/create-marketplace

## Anthropic's directory (claude.ai, Cowork, Claude Code)

One listing reaches all three. Human review.

1. A paid claude.ai plan is required to submit (Pro or Max from your own account; Team and Enterprise need an Owner).
2. `claude plugin validate ./your-plugin --strict` must pass; the portal applies extra rules on top.
3. Check the component support table: some plugin parts are Claude Code-only. Skills load everywhere.
4. Submit at https://claude.ai/directory/manage.

The built-in `claude-plugins-official` marketplace does not take submissions; it is arranged through an Anthropic partner contact.

Docs: https://claude.com/docs/plugins/submit · https://claude.com/docs/plugins/pre-submission-checklist

## claude.ai zip upload (one person or one organisation)

Zip the skill folder and upload it under Customize > Skills. Code execution and file creation must be switched on in Settings > Capabilities or the skill is greyed out. Team and Enterprise owners can provision a skill for everyone from Organization settings > Skills. Limit 50 MB. (Menu names come from secondary guides; confirm in the app.)

## ChatGPT and Codex: universal plugin directory

OpenAI distributes skills inside plugins; one public plugin is listed for both ChatGPT and Codex.

Local use without a plugin — Codex reads skills from:
- `$REPO_ROOT/.agents/skills` (shared with everyone on the repo)
- `$HOME/.agents/skills` (personal)

Plugin layout (root `plugin.json`, skills discovered from `skills/`):
```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "my-skills",
  "version": "1.0.0",
  "description": "What the skills do, in one line",
  "extensions": {
    "com.openai": { "interface": { "displayName": "My Skills", "category": "Productivity" } }
  }
}
```

Share without the public directory — a marketplace file in a repo, added with:
```bash
codex plugin marketplace add owner/repo
```

Public listing: submit through the plugin submission portal in the OpenAI Platform dashboard. Reported prerequisites: identity verification for the publisher name and the `api.apps.write` permission. The submission doc page could not be opened when this was written, and most public guidance covers plugins with a connector (MCP server); requirements for a skills-only plugin are **not verified** — read the current "Submit plugins" doc before promising the user a listing.

Optional polish per skill: `agents/openai.yaml` with `interface` (display name, icon, brand colour) and `policy.allow_implicit_invocation`.

Docs: https://developers.openai.com/plugins/build/plugins · https://learn.chatgpt.com/docs/build-skills · https://developers.openai.com/plugins/plugin-guidelines

## Gemini CLI extension

Extensions bundle skills with commands and connectors, live in public GitHub repos, and need no approval from Google; the gallery picks them up. The manifest name and the gallery's inclusion rule were **not verified** here — check https://geminicli.com/docs/extensions/ ("Build Gemini CLI extensions") for the current manifest and release steps before publishing.
