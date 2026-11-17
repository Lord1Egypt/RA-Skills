## Description:

Provides Chinese-language insurance guidance for users with prior illnesses or abnormal health indicators by structuring health questions, querying ZhongMinBao product rules, and comparing relevant insurance options with compliance disclaimers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellonorth](https://clawhub.ai/user/hellonorth)

### License/Terms of Use:

MIT-0

## Use Case:

External users and insurance-support agents use this skill to evaluate insurance options for people with pre-existing conditions, health abnormalities, or non-standard underwriting questions. It helps collect minimal health context, query ZhongMinBao product information, compare other insurer products, and produce cautious Chinese guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share sensitive health history, and normalized health questions can be sent to ZhongAn's API or third-party search.

Mitigation: Ask for explicit consent before external queries, minimize health details, avoid identifiers, and disclose when information leaves the local context.

Risk: A reusable API key is present in source code.

Mitigation: Rotate the key, move it to a secret store, and restrict access before broad deployment.

Risk: Insurance guidance can be incorrect or outdated if product rules, prices, or underwriting criteria change.

Mitigation: Use current authoritative insurer sources, keep compliance disclaimers, and defer final eligibility and claims decisions to the insurer's underwriting or claims process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hellonorth/skills/za-healthguide)
- [Compliance rules](references/compliance-rules.md)
- [ZhongMinBao product reference](references/zhongminbao-products.md)
- [Other insurer product reference](references/other-products.md)
- [ZhongAn insurance product portal](https://ihealth.zhongan.com/wxmp/pages/index)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese-language Markdown with structured product comparisons, underwriting caveats, and compliance disclaimers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include insurer URLs and cautious next steps; should avoid requesting identifiers or detailed medical records.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
