## Description:

Guides users through configuring personal Xianyu and Sam's Club account details for self-service ordering help.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to configure their own Xianyu/Taobao and Sam's Club account details, check local environment setup, and follow a manual self-ordering flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive marketplace cookies or phone numbers may be placed in a shared workspace environment file without a demonstrated need.

Mitigation: Prefer the manual ordering flow and avoid storing real Taobao/Xianyu session cookies for this version; provide account details only when an implemented action requires them and use secure secret storage with revocation guidance.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference environment variable names for account configuration; no structured API output.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
