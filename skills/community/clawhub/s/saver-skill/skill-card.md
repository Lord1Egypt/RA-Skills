## Description:

Saver is a Mainland China shopping assistant that helps agents analyze shopping needs, search JD.com and Taobao/Tmall products, compare prices, and return purchase links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyichu86](https://clawhub.ai/user/chenyichu86)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to clarify product requirements, search JD.com and Taobao/Tmall, compare prices and sorting options, and present purchase links for Mainland China shopping workflows.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Product links may be affiliate or promotional links, and the skill documentation says commission information is not shown to users.

Mitigation: Tell users that purchase links may be affiliate or promotional links before presenting them.

Risk: The skill uses an unauthenticated plaintext remote MCP endpoint for shopping requests.

Mitigation: Avoid sending sensitive shopping details unless the service is moved to authenticated HTTPS and returned links are validated.

## Reference(s):

- [Saver Skill on ClawHub](https://clawhub.ai/chenyichu86/skills/saver-skill)
- [Publisher profile](https://clawhub.ai/user/chenyichu86)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or text product recommendations with linked product names and shopping guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include streamed progress updates, sorted product lists, prices, coupons or subsidy calculations, and affiliate purchase links.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact config.json and SKILL.md declare 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
