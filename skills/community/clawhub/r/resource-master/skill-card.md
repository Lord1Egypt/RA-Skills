## Description:

Resource Master helps agents estimate and summarize hospital server hardware resources from Chinese-language knowledge-base documents, including merged assessments across multiple medical products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellohushuai](https://clawhub.ai/user/hellohushuai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, implementation engineers, and healthcare project teams use this Chinese-language skill to turn hospital scale inputs and selected medical products into server resource estimates, consolidated hardware tables, resource totals, and deployment notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads relevant local kb/ documents, so sensitive or unrelated files in that scope could influence generated estimates.

Mitigation: Keep sensitive or unrelated documents outside the kb/ scope and review the cited source paths in the response.

Risk: Hardware estimates can be inaccurate when knowledge-base documents are stale or project inputs such as outpatient volume, inpatient volume, staff count, or product list are incomplete.

Mitigation: Provide the required sizing inputs and verify final resource tables against current project requirements before procurement or deployment planning.

## Reference(s):

- [Hardware resource sizing template](references/hardware-template.md)
- [ClawHub skill page](https://clawhub.ai/hellohushuai/skills/resource-master)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown tables and concise prose with source-path citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local kb/ documents as supporting evidence for estimates]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
