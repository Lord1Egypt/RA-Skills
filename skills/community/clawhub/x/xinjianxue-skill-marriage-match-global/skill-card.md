## Description:

XinJianXue Marriage & Partner Selection Advisor helps an agent call the XinJianXue paid API to produce relationship, personality, and long-term marriage-fit analysis after explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to request XinJianXue marriage and partner-selection analysis for themselves or explicitly agreed subjects. The skill guides onboarding, credential handling, report API calls, and human-facing delivery of relationship-fit guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the user to provide a sensitive one-time XinJianXue authorization code in the AI chat.

Mitigation: Use the code only for account binding, avoid sharing it outside the current AI interaction, and never store or repeat it in conversation history or configuration files.

Risk: The skill transmits birth, gender, birthplace, and current-location details to www.xinjianxue.com for analysis.

Mitigation: Obtain explicit consent before each analysis, submit only required fields, and do not submit information about another person unless that person has agreed.

Risk: Report calls consume paid service tokens under the user's bound XinJianXue account.

Mitigation: Confirm the user's intent before calling the report endpoint and explain token usage when relevant.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-marriage-match-global)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)
- [XinJianXue service domain](https://www.xinjianxue.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with HTTP request examples and prose guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include translated report summaries and relationship-fit guidance; requires external API credentials and token billing.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
