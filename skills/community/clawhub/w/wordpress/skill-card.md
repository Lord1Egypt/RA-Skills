## Description:

OpenClaw skill that provides a WordPress REST API CLI for posts, pages, categories, tags, users, and custom requests using plain HTTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

Developers and automation operators use this skill to manage WordPress posts, pages, taxonomy entries, and user reads through JSON-in/JSON-out REST API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable WordPress credentials can be exposed if used with non-HTTPS site URLs.

Mitigation: Use HTTPS-only WordPress base URLs and keep credentials out of logs, commits, and shared command history.

Risk: Write, delete, and raw request commands can modify or remove live WordPress content.

Mitigation: Run the skill with a dedicated low-privilege account, stage changes as drafts when possible, and require human review before production delete or raw request operations.

## Reference(s):

- [WordPress REST API Guide](artifact/assets/wordpress-rest-api-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/codedao12/skills/wordpress)
- [Publisher Profile](https://clawhub.ai/user/codedao12)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-oriented CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI writes JSON to stdout and returns a non-zero exit code on errors.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
