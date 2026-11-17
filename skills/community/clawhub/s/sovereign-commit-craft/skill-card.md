## Description:

Analyzes diffs and commit history to produce Conventional Commit messages, changelogs, release notes, PR descriptions, and commit review guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryudi84](https://clawhub.ai/user/ryudi84)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to turn diffs, commit lists, or change descriptions into Conventional Commit messages, changelogs, release notes, PR descriptions, version-bump recommendations, and commit-splitting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install example uses an unpinned npx command.

Mitigation: Install with a trusted or pinned ClawHub CLI version when possible.

Risk: Generated shell commands or release instructions may be inappropriate for a specific repository.

Mitigation: Review generated commands and instructions before running or publishing them.

Risk: Diffs and commit logs can contain secrets or sensitive project information.

Mitigation: Do not paste secrets or sensitive diffs unless sharing them with the agent is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryudi84/skills/sovereign-commit-craft)
- [Keep a Changelog v1.1.0](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning v2.0.0](https://semver.org/spec/v2.0.0.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with plain text and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commit subjects and bodies, changelog sections, release notes, PR templates, version-bump recommendations, and command examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
