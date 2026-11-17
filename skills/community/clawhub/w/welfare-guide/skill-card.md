## Description:

Welfare Guide helps agents route Korean welfare and government benefit questions across nine intents, collect eligibility details, and produce concise or deeper guidance using official Korean welfare sources when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sw326](https://clawhub.ai/user/sw326)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer Korean welfare, childcare, birth support, basic living, youth, senior, disability, application, and beginner questions with condition-aware guidance and official-source reminders.

### Deployment Geography for Use:

South Korea

## Known Risks and Mitigations:

Risk: The skill may discuss sensitive eligibility details such as age, household, income, disability, pregnancy, or region.

Mitigation: Share only the details needed for the welfare question and avoid unnecessary personal data.

Risk: Welfare eligibility and benefit amounts can change or vary by agency and locality.

Mitigation: Confirm final eligibility, amounts, and application requirements with official agencies such as Bokjiro, Government24, the Ministry of Health and Welfare, or the local resident center.

Risk: A data.go.kr API key may be used for official API access.

Mitigation: Store the API key in a private directory with restrictive permissions, such as chmod 600 on the key file.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sw326/skills/welfare-guide)
- [Intent Router](references/intent_router.md)
- [Output Templates](references/output_templates.md)
- [Source Tiers](references/source_tiers.md)
- [data.go.kr](https://www.data.go.kr)
- [Bokjiro Central Welfare API](https://www.data.go.kr/data/15090532/openapi.do)
- [Bokjiro Local Welfare API](https://www.data.go.kr/data/15108347/openapi.do)
- [Subsidy24 API](https://www.data.go.kr/data/15113968/openapi.do)
- [Government24](https://www.gov.kr)
- [Bokjiro](https://www.bokjiro.go.kr)
- [Ministry of Health and Welfare](https://www.mohw.go.kr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables and optional bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Always produces a Flash Layer; Deep-Dive output is used on request or for benefit search, basic living, childcare, and birth support intents.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
