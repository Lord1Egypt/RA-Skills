## Description:

小鹿选房是专业的涵盖全国的房产信息平台，当用户需要找房源（二手房、租房、新房、买房、找房）、选笋盘、比价格、查成交、看小区、查学区、查学校时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangjike](https://clawhub.ai/user/fangjike)

### License/Terms of Use:

MIT-0

## Use Case:

External home seekers and real-estate researchers use this skill through an agent to find homes, compare prices, review transaction information, explore communities, and check school or school-district information in supported Chinese cities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to execute an unpinned npm CLI package.

Mitigation: Review the xiaolu-house npm package and publisher before installation, and prefer a pinned reviewed version.

Risk: The CLI can handle API keys and local configuration.

Mitigation: Use a limited API key and require confirmation before showing, changing, or clearing saved configuration.

Risk: The skill can query an external real-estate service and is subject to rate limits.

Mitigation: Keep requests to the documented one-per-second rate and retry later after 429 responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangjike/skills/xiaolu-house)
- [ClawHub publisher profile](https://clawhub.ai/user/fangjike)
- [xiaolu-house homepage](https://github.com/fanggeek/xiaolu-house)
- [小鹿选房 API key setup](https://www.xiaoluxuanfang.com/claw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and natural-language text with CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include house, community, transaction, school, new-home, mini-program link, and configuration guidance from the xiaolu-house CLI.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
