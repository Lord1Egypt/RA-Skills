## Description:

Format commit messages using the Conventional Commits specification for automated tooling, changelog generation, and semantic versioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to draft, review, or normalize Git commit messages in Conventional Commits format, including scopes, breaking-change markers, and semantic-versioning signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate during broad discussions about commits, not only explicit requests to draft a commit message.

Mitigation: Use it where commit-message guidance is expected, and review generated guidance before treating it as the intended task response.

Risk: Incorrect or overly generic commit-message guidance could reduce changelog quality or semantic-versioning accuracy.

Mitigation: Review proposed commit messages against the actual code change, especially type, scope, and breaking-change notation.

## Reference(s):

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/qui-conventional-commits)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text commit-message guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
