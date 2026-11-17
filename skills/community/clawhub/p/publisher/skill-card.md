## Description:

Make your skills easy to understand and impossible to ignore.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tunaissacoding](https://clawhub.ai/user/tunaissacoding)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill publishers use Publisher to generate clearer skill descriptions and README content, then publish skill releases through GitHub and ClawdHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload the current directory to a public GitHub repository without enough file scoping or secret-safety checks.

Mitigation: Run it only from a reviewed skill directory after removing secrets, private code, .env files, logs, backups, and unreviewed files; add file previews, allowlists, secret scanning, and private-by-default repository creation before broader use.

Risk: Generated descriptions and publishing steps can commit and distribute incorrect or unreviewed skill documentation.

Mitigation: Review the generated one-liner, README content, SKILL.md frontmatter, git diff, and ClawdHub package contents before approving publication.

## Reference(s):

- [GitHub documentation best practices](https://docs.github.com/en/contributing/writing-for-github-docs/best-practices-for-github-docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, shell command output, and edited skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update SKILL.md frontmatter, create or rely on README.md, initialize git, create a public GitHub repository, push repository contents, and publish to ClawdHub after user approval.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
