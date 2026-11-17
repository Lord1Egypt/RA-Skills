## Description:

AI-ready skill to format and publish Markdown articles to WeChat Official Accounts using Wenyan CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caol64](https://clawhub.ai/user/caol64)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, publishers, and agents use this skill to format Markdown articles for WeChat Official Accounts and prepare live publication through Wenyan CLI. It is suited to workflows that need themed article layout, code highlighting, metadata-driven publishing, and media upload handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish live WeChat content and upload images using account credentials.

Mitigation: Inject WeChat credentials securely only at publish time and require explicit final confirmation before running any live publish or upload command.

Risk: The workflow relies on a globally installed third-party Wenyan CLI.

Mitigation: Use an isolated environment and pin and verify the Wenyan CLI version before installation.

Risk: Incorrect metadata, missing images, or IP restrictions can cause failed or unintended publishing behavior.

Mitigation: Validate required YAML frontmatter, confirm referenced image paths, and ensure the environment's outbound IP is allowed in the WeChat account settings before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caol64/skills/wenyan-publish)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and YAML frontmatter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WeChat credentials at publish time and a Wenyan CLI installation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
