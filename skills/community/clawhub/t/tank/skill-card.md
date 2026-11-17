## Description:

储罐CAD图纸生成。当用户说"储罐"、"生成储罐图纸"、"做一个储罐"、"tank"时使用此 skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liv09370](https://clawhub.ai/user/liv09370)

### License/Terms of Use:

MIT-0

## Use Case:

Engineers and external users use this skill to collect tank design parameters in Chinese, calculate tank dimensions through the JXT workflow, and create a guest production sheet for horizontal or vertical tank CAD drawing generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tank design parameters and generated production sheet links are sent to jixietools.com rather than remaining local.

Mitigation: Use only with engineering data approved for that external service; avoid proprietary or confidential inputs unless the service is approved for the user's organization.

Risk: The workflow creates unauthenticated guest production sheet links.

Mitigation: Treat generated guest links as sensitive and share them only with intended recipients.

## Reference(s):

- [ClawHub Tank Skill](https://clawhub.ai/liv09370/skills/tank)
- [Jixietools API Base URL](https://jixietools.com/api/v1)
- [Jixietools Tank Products Endpoint](https://jixietools.com/api/v1/products?category_id=9)
- [Jixietools Guest Production Sheet Endpoint](https://jixietools.com/api/v1/production_sheets/guest_create)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown]

**Output Format:** [Chinese conversational guidance with tables and inline curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-facing tank parameter summaries, calculated values, guest production sheet links, and progress updates.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
