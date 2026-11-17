## Description:

Helps quality-management practitioners decompose company-level quality objectives into department, process, and time-based matrices with SMART checks, and review existing objective documents against ISO 9001:2015 Clause 6.2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external consultants, quality managers, and QMS auditors use this skill to plan measurable quality objectives, map objectives across organizational levels, and identify ISO 9001:2015 Clause 6.2 gaps in existing objective documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Referenced helper scripts and templates may be unavailable in the installed artifact.

Mitigation: Verify that the runtime provides the referenced helpers or adapt the workflow to produce text-only matrices, SMART checks, and audit findings before relying on scripted output.

Risk: Generated objective values, decomposition factors, and audit findings may be mistaken for final management decisions or certification audit results.

Mitigation: Have qualified quality-management personnel confirm objective values, business assumptions, ISO 9001 applicability, and any remediation plan before adoption.

Risk: Missing baseline data, organizational structure, or quality policy text can make decomposition and conformance findings incomplete.

Mitigation: Require the user to provide required inputs where possible and clearly label unsupported assumptions as for reference or pending confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-qms-objective-decomposition)
- [Server-resolved source repository](https://github.com/duding-engicool/skill-qms-objective-decomposition)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with tables, structured findings, and inline shell commands when helper scripts are available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Marks missing business inputs as for reference or pending confirmation, and keeps final target values subject to user review.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
