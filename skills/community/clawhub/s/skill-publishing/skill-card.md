## Description:

Guide to publishing and sharing Hermes skills through ClawHub, including safe login practices, release hygiene, and security scan preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuxuclassmate](https://clawhub.ai/user/xuxuclassmate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill as a concise checklist for preparing, publishing, updating, and cleaning up Hermes skills on ClawHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrative examples include delete and merge commands that can change published skill state.

Mitigation: Review the target slug and intended published state before running delete or merge commands.

Risk: Login examples handle a ClawHub token.

Mitigation: Use the private token-reading pattern only with tokens intentionally granted to the ClawHub CLI, then unset the token variable after login.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuxuclassmate/skills/skill-publishing)
- [ClawHub publisher profile](https://clawhub.ai/user/xuxuclassmate)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise publishing checklist with command examples.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
