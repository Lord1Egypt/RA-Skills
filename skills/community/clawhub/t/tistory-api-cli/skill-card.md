## Description:

Tistory API CLI helps agents guide users through installing and using an unofficial command-line tool for reading, updating, deleting, categorizing, and uploading images to Tistory blog posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical bloggers, and agents use this skill to produce terminal-oriented guidance for managing Tistory blog content with the tistory-api-cli package. It is most useful when a workflow needs concise install steps, environment variable setup, and example commands for post, category, and image operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install unpinned external code that can use Tistory credentials.

Mitigation: Install the CLI in an isolated tool environment, verify the PyPI package publisher and version before use, and grant only the narrowest available Tistory token.

Risk: Update, delete, and upload commands can affect live blog content.

Mitigation: Review generated commands before execution and test changes against non-critical posts or backups before applying them to important content.

## Reference(s):

- [Tistory API CLI on ClawHub](https://clawhub.ai/chloepark85/skills/tistory-api-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and environment variable names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include package installation commands, Tistory environment variable setup, and command examples for blog content operations.]

## Skill Version(s):

0.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
