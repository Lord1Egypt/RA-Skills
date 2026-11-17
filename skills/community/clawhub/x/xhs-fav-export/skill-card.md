## Description:

Exports the current user's Xiaohongshu favorites as local Markdown notes with text, original links, and image or video URLs, supporting batched and resumable backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatmind](https://clawhub.ai/user/fatmind)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals use this skill to back up and search their own Xiaohongshu favorites offline, exporting selected batches to a local Markdown knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The exporter uses the logged-in Chrome Xiaohongshu session and saves favorites as unencrypted local files.

Mitigation: Install only if you trust the publisher, and export sensitive favorites to a private, non-synced folder.

Risk: An undocumented obfuscated helper could forward selected prompts or file contents to an endpoint.

Mitigation: Do not invoke wc3-code.mjs unless you have inspected or removed it and explicitly trust its endpoint.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/fatmind/skills/xhs-fav-export)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Text]

**Output Format:** [One Markdown file per exported note, a JSON summary, and a JSON status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports links to images and videos rather than downloading media; supports offset and count for batches.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
