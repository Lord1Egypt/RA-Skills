## Description:

Generates, filters, and explains seven-day Chinese listed-company violation weekly reports from the 聚源违规案例库, with deliverables in Word, JSON, or Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoeluli7459-dev](https://clawhub.ai/user/zoeluli7459-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to produce weekly summaries of listed-company violation cases, affected companies, penalty objects, violation matters, penalty details, and legal bases from the configured 聚源违规案例库 source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Externally delivered Word reports automatically include fixed 董小屿违规案例库 branding and the dxy-aiagent.com source URL in visible output and document metadata.

Mitigation: Use the Word output only where that attribution is acceptable, and review generated documents before distribution.

Risk: Reports are constrained to 聚源违规案例库 fields and may contain partial or review_required case quality states when source fields are missing or conflict.

Mitigation: Review JSON or Markdown quality fields before relying on the report for compliance or business decisions, and do not treat missing fields as confirmed absence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoeluli7459-dev/skills/weekly-report-companies-violations)
- [违规案例周报字段参考](references/schema.md)
- [董小屿违规案例库](https://www.dxy-aiagent.com/website/weigui)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Chinese Markdown, JSON, or .docx Word report generated from structured case data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Word output uses fixed report formatting, internal hyperlinks, document metadata, and fixed 董小屿违规案例库 attribution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
