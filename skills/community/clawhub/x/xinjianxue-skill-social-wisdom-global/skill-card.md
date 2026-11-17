## Description:

Provides a XinJianXue Social Savvy Advisor workflow for relationship-sensitive social guidance, using the XinJianXue API as reference data only after explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill for users who explicitly request Social Savvy Advisor help with social etiquette, relationship-sensitive wording, gift-giving, favors, and polite refusals. The skill is intended for external users who consent to XinJianXue analysis and understand that API calls consume service tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the user to paste a sensitive one-time XinJianXue authorization code into chat during onboarding.

Mitigation: Ask for the code only after explicit consent, explain that it is sensitive and single-use, and use it only for the official XinJianXue account-binding flow.

Risk: The skill stores credentials for a paid external API and uses them for later calls under the user's account identity.

Mitigation: Store the license key and API key only in scoped credential storage such as an OS keychain or environment secret store, never in chat, configuration files, or long-term memory.

Risk: Using the report API sends birth, gender, birthplace, and current-location details to www.xinjianxue.com and consumes service tokens.

Mitigation: Confirm user understanding before each analysis, collect only required fields, disclose token use, and avoid API calls for casual chat or unconsented third-party analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-social-wisdom-global)
- [XinJianXue service website](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Configuration]

**Output Format:** [Markdown or plain text social guidance with concise setup and credential-handling instructions when onboarding is required]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-facing consent prompts, missing-information requests, translated analysis, and masked credential references; does not store returned reports.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
