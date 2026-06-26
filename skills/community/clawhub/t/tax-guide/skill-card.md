## Description: <br>
Provides Korean tax and tax-saving guidance by routing questions across 10 tax intents and producing Flash or Deep-Dive reports grounded in Korean law and official tax sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sw326](https://clawhub.ai/user/sw326) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users ask Korean tax questions about filing, deductions, VAT, property tax, inheritance or gift tax, withholding, disputes, and beginner tax concepts. The skill helps an agent classify the request, gather needed facts, consult official-source tiers, and return informational guidance with clear disclaimers. <br>

### Deployment Geography for Use: <br>
South Korea <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat general tax guidance as professional tax advice. <br>
Mitigation: Keep outputs informational, include the tax-advice disclaimer, and direct users to NTS, Hometax, or a tax professional for case-specific decisions. <br>
Risk: Tax rates, deadlines, deductions, and forms can change. <br>
Mitigation: Verify current amounts and deadlines against official Korean tax sources before acting. <br>
Risk: Tax questions may involve sensitive identity or financial information. <br>
Mitigation: Avoid collecting unnecessary identifiers, credentials, resident registration numbers, or full financial records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sw326/tax-guide) <br>
- [Intent router](references/intent_router.md) <br>
- [Output templates](references/output_templates.md) <br>
- [Source tiers](references/source_tiers.md) <br>
- [Tax guide playbook](playbook.md) <br>
- [Korean tax law reference](https://www.law.go.kr/법령/소득세법) <br>
- [National Tax Service](https://www.nts.go.kr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown tax guidance with Flash and optional Deep-Dive sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes informational-tax disclaimers and should be verified against NTS, Hometax, law.go.kr, or a tax professional before users act on deadlines, amounts, or case-specific interpretations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
