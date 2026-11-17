## Description:

US import tariff toolkit for finding HTS/HS codes, computing stacked U.S. duties and fees, estimating landed cost, checking refund eligibility and deadlines, and locally parsing ACE Form 7501 entry summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voltaudits](https://clawhub.ai/user/voltaudits)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and trade operations teams use this skill to answer U.S. import duty, customs classification, landed-cost, Section 301/232 tariff, and tariff-refund deadline questions. It can run a bundled Node.js tariff engine locally and can provide command guidance for live lookups when offline data is insufficient.

### Deployment Geography for Use:

Global (for U.S. import tariff workflows)

## Known Risks and Mitigations:

Risk: The skill's offline and privacy claims can conflict with instructions that contact invoicetariff.com for live lookups or direct users to web tools.

Mitigation: Use local commands for sensitive customs documents and allow live lookups or website handoff only when that data flow is acceptable.

Risk: Tariff, refund, and deadline outputs can affect filing or money decisions.

Mitigation: Verify outputs against official sources or a customs professional before acting on tariff or refund guidance.

## Reference(s):

- [Data & Sources](references/data-and-sources.md)
- [ClawHub skill page](https://clawhub.ai/voltaudits/skills/us-tariff-lookup)
- [InvoiceTariff homepage](https://invoicetariff.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command outputs include ruleset version, data-as-of date, caveats, and disclaimers when tariff or refund calculations are involved.]

## Skill Version(s):

0.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
