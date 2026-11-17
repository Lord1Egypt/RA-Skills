## Description:

Saves WeChat public-account articles as Markdown in an Obsidian knowledge base, with optional Feishu table tracking and optional Simplified Chinese sprout-note generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[violin86318](https://clawhub.ai/user/violin86318)

### License/Terms of Use:

MIT-0

## Use Case:

External users and knowledge workers use this skill to archive WeChat public-account articles into a local Obsidian Markdown collection and optionally track article links in Feishu. It can also generate a separate Simplified Chinese reflection note from the saved article content when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned shell command examples may run changing third-party code when fetching articles or managing records.

Mitigation: Review commands before use and replace `npx -y bun` and `lark-cli` examples with pinned, verified executables and safe argument handling.

Risk: Configured Feishu credentials can create or delete table records.

Mitigation: Use least-privilege Feishu credentials, avoid enabling delete access unless needed, and require explicit user confirmation before deletion.

Risk: Article URLs or content may be sent to Jina Reader, Feishu, browser tooling, and a model provider.

Mitigation: Use only trusted article URLs and avoid processing sensitive content unless those services are approved for the data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, Feishu record fields, and a concise Markdown completion message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are Simplified Chinese by default; optional Feishu and sprout-note outputs depend on local configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
