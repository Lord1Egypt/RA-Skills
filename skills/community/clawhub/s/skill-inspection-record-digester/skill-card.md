## Description:

Turns photographed or scanned inspection-record tables into reviewed structured records, a Markdown analysis report, and CSV data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality, equipment, and audit teams use this skill to convert batches of photographed or scanned inspection tables into user-reviewed structured records, then generate summary analysis for pass rates, anomalies, trends, and top issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Low-confidence or unclear visual recognition could produce incorrect inspection data if accepted without review.

Mitigation: Require user confirmation or correction before analysis; do not fill unclear fields.

Risk: Generated local outputs may overwrite existing report.md or records.csv in a reused output directory.

Mitigation: Confirm the output directory before running the digest step and avoid reusing directories with files that should be preserved.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/duding-engicool/skill-inspection-record-digester)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-inspection-record-digester)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Conversational guidance plus Markdown report and CSV records files from reviewed structured JSON input]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation of low-confidence recognition fields before analysis; writes local report.md and records.csv.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
