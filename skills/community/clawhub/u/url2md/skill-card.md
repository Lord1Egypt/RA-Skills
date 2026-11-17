## Description:

URL to Markdown converts static HTTP/HTTPS web pages into clean Markdown, with optional batch conversion, YAML frontmatter, templates, filename generation, and image downloading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rwonly](https://clawhub.ai/user/rwonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and knowledge-base maintainers use this skill to convert individual web pages or URL lists into Markdown files for documentation, archiving, notes, and static content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL fetching is broad and can reach local or internal resources when supplied with crafted URLs.

Mitigation: Use trusted public HTTP/HTTPS URLs only, and avoid running the skill in environments that can reach internal services, cloud metadata endpoints, or sensitive local resources.

Risk: Batch mode and image downloads can trigger many outbound requests and write many files.

Mitigation: Review URL lists before use, limit batch inputs, choose output directories deliberately, and use --download-images only when the remote content and destination are trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rwonly/skills/url2md)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown text or Markdown files, optionally with YAML frontmatter and local image assets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports stdout output, single-file output, batch directory output, custom templates, generated filenames, and optional image downloads.]

## Skill Version(s):

2.1.2 (source: server evidence and script __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
