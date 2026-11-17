## Description:

A skill that creates new Claude skills and automatically shares them on Slack using Rube for seamless team collaboration and skill discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javotillo](https://clawhub.ai/user/javotillo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team members use this skill to create, validate, package, and share Claude skills with Slack notifications for team visibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically post newly created skill metadata and file links to Slack without a clear per-use confirmation or recipient review step.

Mitigation: Confirm the Slack workspace and target channel before use, and add a manual review step before sharing skill names, descriptions, paths, or links that could reveal sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/javotillo/skills/skill-share)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated skill files, package artifacts, and Slack notification content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference distributable skill packages and team notification metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
