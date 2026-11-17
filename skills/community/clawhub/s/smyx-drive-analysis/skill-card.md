## Description:

Analyzes driver videos to identify unsafe driving behaviors and produce structured safety analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Drivers and road safety educators can submit a local or linked driving video to review behaviors such as fatigue, distraction, and seatbelt use. The skill returns structured findings, safety suggestions, and links to reports, and can retrieve prior reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Driver video may be processed remotely, and using the service may involve account registration and credential storage.

Mitigation: Review the service's privacy and credential practices and obtain appropriate consent before submitting footage.

Risk: The no-analysis option may not prevent analysis.

Mitigation: Do not rely on that option as a privacy control; avoid submitting sensitive footage unless remote analysis is acceptable.

Risk: The security scan was partial because a referenced local path was missing, so its evidence is incomplete.

Mitigation: Treat the scan as incomplete and review the missing-path behavior before installation.

## Reference(s):

- [Skill API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-drive-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured driving behavior report with findings, safety suggestions, and report links; JSON or Markdown output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can provide a concise or detailed report and save results to a file.]

## Skill Version(s):

1.0.19 (source: server-resolved release; artifact frontmatter says 1.0.27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
