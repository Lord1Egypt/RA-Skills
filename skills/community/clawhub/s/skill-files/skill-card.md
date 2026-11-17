## Description:

Review UI code for Web Interface Guidelines compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[divyamprusty](https://clawhub.ai/user/divyamprusty)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and UI engineers use this skill to review interface code against Web Interface Guidelines and receive concise file-and-line findings for remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches a mutable external guidelines document on each review, so behavior and output criteria may change without a skill release.

Mitigation: Review the fetched guidelines before relying on findings, or use a version that vendors or pins the guidelines source.

Risk: The fetched document includes review and output instructions that could influence agent behavior beyond static skill contents.

Mitigation: Treat remote guideline text as untrusted reference material and keep final remediation changes under human review.

## Reference(s):

- [Web Interface Guidelines command source](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md)
- [ClawHub skill page](https://clawhub.ai/divyamprusty/skills/skill-files)
- [Publisher profile](https://clawhub.ai/user/divyamprusty)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with concise file:line findings and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings depend on the current contents of the external guidelines document fetched at review time.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
