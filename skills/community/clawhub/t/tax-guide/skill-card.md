## Description:

Korea-focused tax guidance skill that routes common tax questions across ten intents and produces concise Flash guidance with optional Deep-Dive analysis based on official tax-law and National Tax Service sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sw326](https://clawhub.ai/user/sw326)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer Korean tax, filing, deduction, VAT, property tax, inheritance, gift tax, withholding, and tax-dispute questions with structured guidance. It is intended for general information and should not replace advice from a qualified tax professional or official tax authority.

### Deployment Geography for Use:

South Korea

## Known Risks and Mitigations:

Risk: Tax rates, deadlines, and filing procedures may be outdated or incomplete for a user's exact facts.

Mitigation: Treat outputs as general information and verify current requirements against official National Tax Service, HomeTax, or law.go.kr sources before acting.

Risk: Broad Korean tax triggers may route adjacent questions into tax mode when clarification would be more appropriate.

Mitigation: Confirm the tax topic and required facts when the user's request is ambiguous or missing key details.

Risk: Users may disclose unnecessary personal financial details while asking for tax guidance.

Mitigation: Ask only for the minimum facts needed and avoid collecting sensitive identifiers or unnecessary account-level details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sw326/skills/tax-guide)
- [Publisher profile](https://clawhub.ai/user/sw326)
- [Intent router](artifact/references/intent_router.md)
- [Output templates](artifact/references/output_templates.md)
- [Source tiers](artifact/references/source_tiers.md)
- [National Tax Service](https://www.nts.go.kr)
- [Korean law portal](https://www.law.go.kr/법령/소득세법)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Korean Markdown guidance with a Flash section and optional Deep-Dive section]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a general-information tax disclaimer and asks a single clarification question when required tax facts are missing.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
