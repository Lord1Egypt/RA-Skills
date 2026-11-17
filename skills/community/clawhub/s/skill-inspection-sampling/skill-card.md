## Description:

A Chinese-language inspection sampling helper for designing sampling schemes, parsing inspection data, generating sampling plans, tracking records, and producing statistical reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality engineers, inspection teams, and developers use this skill to prepare local inspection sampling workflows, convert inspection datasets, create sampling results, and summarize sampling quality. It should not be treated as proof of GB/T2828 compliance without independent validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation may overstate GB/T2828 coverage while the reviewed scripts implement generic sampling methods.

Mitigation: Use independent statistical and compliance review before relying on generated plans for GB/T2828 or regulated inspection decisions.

Risk: The skill reads local inspection datasets and writes JSON outputs that may contain sensitive product or quality data.

Mitigation: Run it in a controlled workspace, review generated files before sharing, and apply the same data-handling controls used for the source inspection records.

Risk: Audit records can be retained under ./sampling_records/ when recording is enabled.

Mitigation: Decide retention requirements before use and remove or archive generated records according to the user's quality and privacy policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-inspection-sampling)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)
- [Server-resolved source repository](https://github.com/duding-engicool/skill-inspection-sampling)
- [Inspection sampling data format specification](references/format_spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON files]

**Output Format:** [Markdown guidance with shell commands and local JSON artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads CSV, Excel, and JSON inputs; writes parsed data, sampling results, statistical reports, and optional audit records under ./sampling_records/.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
