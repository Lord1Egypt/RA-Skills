## Description:

Helps non-technical users deploy websites on Tencent Cloud and manage DNS, certificates, CDN, and servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claw-school](https://clawhub.ai/user/claw-school)

### License/Terms of Use:

MIT-0

## Use Case:

People without cloud-operations experience use this skill to put websites online, configure domain routing and HTTPS, and manage Tencent Cloud delivery and hosting. Purchases, identity verification, and regulatory filing remain with the user.

### Deployment Geography for Use:

Global; mainland China hosting and acceleration may require ICP registration.

## Known Risks and Mitigations:

Risk: Long-lived cloud credentials allow changes to DNS, CDN, and server settings.

Mitigation: Use the limited agent-ops sub-account policy and keep only intended servers in scope.

Risk: Remote root commands can alter or delete data on managed servers.

Mitigation: Review and approve server commands that change data before execution.

Risk: An added SSH key can leave durable server access.

Mitigation: Remove any SSH key the agent adds when it is no longer needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/claw-school/skills/tencentcloud-deploy-web)
- [Publisher homepage](https://claw-school.com)
- [Deployment routes](references/routes.md)
- [Human action cards](references/human-cards.md)
- [Source notes](references/sources.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Conversational guidance and action cards with commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide cloud configuration changes and remote server operations.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
