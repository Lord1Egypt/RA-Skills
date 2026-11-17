## Description:

Save web articles from multiple sources to Obsidian with auto summaries, tags, local images, duplicate detection, and optional user notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vlalamoon](https://clawhub.ai/user/vlalamoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to convert web articles into Obsidian Markdown notes with summaries, tags, local images, duplicate detection, and optional personal notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied article URLs, including query parameters, may be sent to a third-party reader service.

Mitigation: Use public, non-sensitive URLs only, and remove or disable the Jina Reader fetch path before processing private, signed, intranet, or work-document links.

Risk: The script fetches remote article pages and images without explicit network-scope controls.

Mitigation: Review the target URLs and configured Obsidian output paths before execution, and run the skill only in an environment where outbound network access is acceptable.

Risk: Downloaded remote images are written into the configured Obsidian attachments directory.

Mitigation: Inspect the configured attachments path and use a dedicated vault or staging directory before syncing saved content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vlalamoon/skills/save-to-obsidian-publish)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown files with YAML frontmatter, generated summaries, tags, localized image links, and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes article notes to the configured Obsidian directory, stores downloaded images under an attachments directory, and records saved URLs for duplicate detection.]

## Skill Version(s):

2.1.0 (source: server release metadata, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
