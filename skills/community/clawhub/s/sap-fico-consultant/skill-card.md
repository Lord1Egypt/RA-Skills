## Description:

Provides expert SAP FICO consulting with configuration, troubleshooting, integration, and S/4HANA migration support using precise French SAP terminology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chanfouricc](https://clawhub.ai/user/chanfouricc)

### License/Terms of Use:


## Use Case:

SAP finance and controlling teams use this skill to get French technical guidance for FI/CO configuration, troubleshooting, cross-module integration, period-end work, and ECC to S/4HANA migration questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic activation may trigger the SAP FI/CO persona in mixed conversations because the keyword list includes generic business terms such as assessment, distribution, settlement, and closing.

Mitigation: Review and narrow the trigger keywords for shared bots, or require the manual SAP trigger where accidental activation would be disruptive.

Risk: The skill is designed for French technical SAP terminology and may surprise users expecting another language.

Mitigation: Enable it only in contexts where a French SAP FI/CO assistant is intended, or clearly route non-French users to another assistant.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chanfouricc/skills/sap-fico-consultant)
- [Publisher profile](https://clawhub.ai/user/chanfouricc)
- [Skill documentation](artifact/SKILL.md)
- [Skill configuration](artifact/skill.json)
- [System prompt](artifact/system_prompt.md)
- [Few-shot examples](artifact/examples.json)
- [SAP FI/CO T-code index](artifact/tcodes_index.md)
- [SAP FI/CO table index](artifact/tables_index.md)
- [SAP FI/CO error code reference](artifact/error_codes.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions]

**Output Format:** [French Markdown response with SAP T-codes, tables, steps, integration notes, and S/4HANA considerations when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Skill configuration targets concise responses up to 350 words and uses ABAP snippets only when needed.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
