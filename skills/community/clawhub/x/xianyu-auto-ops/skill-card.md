## Description:

Bilingual Xianyu listing and lightweight operations workflow for second-hand goods, side-hustle products, and marketplace distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinhuadeng](https://clawhub.ai/user/jinhuadeng)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace sellers and operators use this skill to create, optimize, and batch-produce bilingual Xianyu listing packages, buyer replies, pricing angles, image prompts, and posting checklists. It can also normalize user-provided CSV product data into compact listing inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated listing copy or pricing may contain inaccurate product condition, service scope, or negotiation claims.

Mitigation: Review pricing, condition disclosures, and service claims before posting publicly.

Risk: The CSV helper processes local files provided by the user.

Mitigation: Run it only on CSV files intentionally supplied for listing generation.

## Reference(s):

- [Xianyu Auto Ops Playbook](references/playbook.md)
- [AI Services / Training / Installation Template](references/ai-services-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with optional inline shell commands and JSON from the CSV helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is bilingual Chinese and English; batch mode keeps each item compact and labels assumptions.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
