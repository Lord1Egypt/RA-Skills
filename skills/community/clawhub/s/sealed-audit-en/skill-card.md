## Description:

For investment due diligence, supplier audits, internal-control and data-compliance checks — the reviewer seals its checking logic into a package for the auditee, who runs it against its local database and returns only a summary. Data never leaves the auditee; the logic is never readable by the auditee. Built on MGC Blackbox 1.6.0 with a runnable minimal example.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT

## Use Case:

Reviewers use the skill to prepare privacy-conscious audit packages for investment due diligence, supplier qualification, internal controls, and compliance checks. Auditees run the checks against local data and return a summary of findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags that scripts may run with the operator's permissions and that the skill declares no tool limits; the finding is suspicious, not malicious.

Mitigation: Review the package source and verify its SHA-256 before execution; run it with only the file and network access it needs.

Risk: The security review is incomplete because some local path references could not be resolved.

Mitigation: Resolve and review referenced files before deployment, then assess the complete package in the intended environment.

## Reference(s):

- [ClawHub release](https://clawhub.ai/zkeviny/skills/sealed-audit-en)
- [MGC Blackbox project](https://github.com/zkeviny/MGC-Blackbox)
- [MGC Blackbox issue tracker](https://github.com/zkeviny/MGC-Blackbox/issues)

## Skill Output:

**Output Type(s):** [Code, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Python audit scripts, JSON finding summaries, and Markdown task briefs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The example result contains a conclusion and rule counts; audit data stays local.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
