# openclaw-skill-x-management

Draft-first X/Twitter account management skill for OpenClaw.

ClawHub: [X Management skill](https://clawhub.ai/princebansal/skills/x-management)

Companion plugin: [OpenClaw X Plugin](https://clawhub.ai/princebansal/plugins/openclaw-plugin-x)

Source: [GitHub repository](https://github.com/princebansal/openclaw-skill-x-management)

## Release notes

### 0.1.6 (next source release; not published)
- Add the current ClawHub listing as standard OpenClaw skill homepage metadata.
- Document compatibility with the current OpenClaw skill format and clarify that this text-only skill has no plugin SDK/runtime API dependency.

### 0.1.5
- Clarify that media uploads are immediate external actions and require a specific user-authorized file and account.

This skill is the agent-side workflow layer that pairs with the `openclaw-plugin-x` plugin.

## OpenClaw compatibility

This is a text-only AgentSkills-format `SKILL.md`; it does not import or call the OpenClaw plugin SDK and has no Gateway/plugin API version floor of its own. It is authored against the current OpenClaw skill frontmatter and loading format and checked alongside the companion plugin targeting OpenClaw 2026.9.7. The plugin must be installed and enabled for the X tools described below to be available. The `homepage` frontmatter field links directly to this ClawHub listing.

## What this skill does

It teaches the agent to use the X plugin safely:
- gather context before drafting when needed
- fetch follower/account graph context when monitoring or tracking account changes
- use exact `accountId` values for multi-account sessions and drafts
- verify non-default accounts with `x_account_me` before publish
- prefer timeline search tools for older own-post lookup
- create drafts instead of publishing directly
- require explicit user approval before publish
- keep reads, drafting, and publish decisions clearly separated

## Intended pairing

Use this skill together with the X plugin:
- plugin = auth, reads, durable drafts, approval state, publish primitive
- skill = judgment, research, tone, workflow, and safety behavior

## Install

After publishing to ClawHub, install with:

```bash
openclaw skills install @princebansal/x-management
```

Then start a new OpenClaw session so the skill is loaded.

## Plugin requirement

This skill is designed to work with the OpenClaw X plugin. Without the plugin, the workflow instructions remain useful, but the tool surface will not be available.

## Files

- `SKILL.md` — primary skill instructions

## Publish

Example ClawHub publish flow:

```bash
clawhub skill publish ./openclaw-skill-x-management \
  --slug x-management \
  --name "X Management" \
  --version 0.1.6 \
  --tags latest
```

## Status

Usable now for the draft-first workflow that matches the current plugin capabilities, including multi-account operation, follower-list reads, post search, media upload, thread publish, and approval-gated publishing.

## License

MIT
