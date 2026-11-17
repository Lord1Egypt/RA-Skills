## Description:

Controls Xiaomi Home devices over a local LAN with miiocli, including status checks, power toggles, and MIOT property updates for supported smart-home devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiqiezhenxi](https://clawhub.ai/user/yiqiezhenxi)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to translate natural-language Xiaomi smart-home requests into miiocli commands for local LAN device control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaomi device tokens can grant local control of smart-home devices if exposed.

Mitigation: Store tokens in a dedicated secrets mechanism outside shared Markdown files, repositories, and chat logs.

Risk: The advertised token extractor is not included in the artifact supplied for review.

Mitigation: Do not rely on the extractor until the actual script is supplied and reviewed.

Risk: The install command uses an unpinned dependency path and a dependency-version fix.

Mitigation: Review and pin install dependencies before using the skill.

Risk: Commands can control heaters, smart plugs, rice cookers, and similar appliances.

Mitigation: Use extra care with appliance-control commands and confirm target devices before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yiqiezhenxi/skills/xiaomi-home-skill)
- [Publisher Profile](https://clawhub.ai/user/yiqiezhenxi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may include local device IP addresses, Xiaomi tokens, and MIOT property identifiers supplied by the user.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
