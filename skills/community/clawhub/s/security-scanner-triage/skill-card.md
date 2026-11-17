## Description:

Triage security and virus scanner findings for skills and automations by separating scanner claims into confirmed issues, partial findings, and false positives with remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okikesolutions](https://clawhub.ai/user/okikesolutions)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and skill maintainers use this skill to triage scanner reports for skills and automations, prioritize real issues, identify false positives, and prepare a concrete remediation plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to inspect scanner reports and security-relevant files, which may include sensitive configuration or credentials.

Mitigation: Run it only in workspaces where security review is intended and continue redacting secrets, including .env values, from outputs.

Risk: Triage output may incorrectly classify scanner claims or understate security impact.

Mitigation: Require source-backed evidence for each claim and review the risk ranking and patch plan before applying changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/okikesolutions/skills/security-scanner-triage)
- [Publisher Profile](https://clawhub.ai/user/okikesolutions)
- [Security Triage Output Template](references/output-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown structured as scanner claim map, evidence, risk ranking, patch plan, data-routing distinction, and re-scan checklist.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill emphasizes source-backed triage, secret redaction, and separating data-routing transparency issues from security-impact issues.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
