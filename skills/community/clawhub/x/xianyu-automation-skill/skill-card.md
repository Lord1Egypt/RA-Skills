## Description:

Enterprise-grade automated operations for Xianyu stores with full lifecycle management, confirmation safeguards, and an intelligent decision engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crab-xieyujin](https://clawhub.ai/user/crab-xieyujin)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, store operators, and developers use this skill to configure and automate Xianyu store operations such as product lifecycle management, pricing strategy, order workflows, and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates account-changing Xianyu store operations while advertised safety limits and success reporting are not fully enforced by the included code.

Mitigation: Review carefully before installing, keep manual approval or dry-run controls at the dependency layer, and avoid unattended production use until limits and reporting are enforced and tested.

Risk: Automation requires Xianyu application credentials and can affect live store products, prices, or orders through dependent skills.

Mitigation: Use a dedicated low-permission Xianyu key, store secrets outside the skill, rotate credentials regularly, and monitor operation logs for unexpected changes.

## Reference(s):

- [Goofish / Xianyu Open Platform](https://www.goofish.pro)
- [ClawHub Source Listing](https://clawhub.com/skills/xianyu-automation)
- [ClawHub Skill Page](https://clawhub.ai/crab-xieyujin/skills/xianyu-automation-skill)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with Python-oriented automation examples and configuration requirements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XIAN_YU_APP_KEY and XIAN_YU_APP_SECRET; depends on xianyu-api-client-skill and xianyu-product-manager-skill.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
