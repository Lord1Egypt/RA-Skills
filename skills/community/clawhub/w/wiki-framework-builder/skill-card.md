## Description:

Builds Chinese consulting-style report frameworks from a scoped research handoff, producing a client-facing Word framework, matching Markdown framework, JSON handoff, and concise chat summary while keeping internal routing codes out of external deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leadleo](https://clawhub.ai/user/leadleo)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, consultants, and agent workflows use this skill after a research scope has been defined to turn the handoff into a structured Chinese consulting or government-style report framework. It is intended for market insight, feasibility, investment, ranking, policy, and strategy framework drafting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed for Chinese consulting and government-style deliverables, which may not match workflows that require English or bilingual output.

Mitigation: Confirm language expectations before use and adapt the handoff or prompt if English or bilingual deliverables are required.

Risk: A DOCX is generated from a handoff JSON file; using the wrong handoff can produce an inaccurate client-facing framework.

Mitigation: Run the DOCX generation step only on the intended report_framework_handoff.json and review the generated Word and Markdown outputs before sharing.

## Reference(s):

- [Engineering dimension database](references/engineering_dimension_database.md)
- [External framework standard](references/external_framework_standard.md)
- [Framework generation rules](references/framework_generation_rules.md)
- [Output contract](references/output_contract.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Chinese chat summary plus Markdown, JSON handoff, and DOCX report framework files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Word file is generated from report_framework_handoff.json and should match the external-facing Markdown framework.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
