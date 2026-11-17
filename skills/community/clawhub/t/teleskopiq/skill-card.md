## Description:

Create, edit, and manage Teleskopiq YouTube scripts, AI conversations, metadata, thumbnails, history, and publishing schedules through its authenticated API with browser OAuth or an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nethunter](https://clawhub.ai/user/nethunter)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and their agents use this skill to draft and manage YouTube content in Teleskopiq, including scripts, AI-assisted revisions, thumbnails, metadata, and publishing schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An authorized agent can change or permanently delete channel scripts through Teleskopiq.

Mitigation: Require clear user intent for destructive actions; review existing content and history before edits or retries.

Risk: OAuth tokens or API keys grant access to channel content if exposed or over-scoped.

Mitigation: Prefer narrowly scoped OAuth, use read-only access for review tasks, and keep credential files private.

## Reference(s):

- [Teleskopiq skill release](https://clawhub.ai/nethunter/skills/teleskopiq)
- [Teleskopiq homepage](https://teleskopiq.com)
- [API inputs and additional operations](artifact/references/api.md)
- [OAuth and MCP guidance](artifact/references/oauth.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Markdown content and guidance; JSON results from the Teleskopiq client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or change remote channel content when authorized.]

## Skill Version(s):

1.3.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
