## Description:

Browse, search, and annotate regulations via the RegMapper API. Use when asked about regulations, rules, compliance requirements, project annotations, or comparing regulation versions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ogruenig](https://clawhub.ai/user/ogruenig)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research regulations, inspect rule structure and content, compare regulation versions, and manage project-scoped review comments in RegMapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A RegMapper API token can expose projects and comments available to the token holder.

Mitigation: Use a least-privilege token where possible and keep REGMAPPER_API_TOKEN out of source control.

Risk: Creating or updating project comments persists changes in RegMapper.

Mitigation: Review agent actions before write operations and only write comments when the selected project grants write access.

## Reference(s):

- [RegMapper](https://regmapper.net)
- [RegMapper API schema](https://www.regmapper.net/api/v1/schema/)
- [RegMapper account signup](https://www.regmapper.net/account/signup/)
- [ClawHub regmapper listing](https://clawhub.ai/ogruenig/skills/regmapper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTTP examples, shell commands, and summarized API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REGMAPPER_API_TOKEN; comment creation and updates depend on the token user's project permissions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
