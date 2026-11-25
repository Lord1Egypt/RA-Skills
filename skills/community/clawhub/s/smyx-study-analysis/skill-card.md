## Description:

Analyzes videos of children's and students' study behavior and returns structured reports with observations and family education suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and educators can submit a study video to review observed focus, posture, and study habits and receive family education suggestions for reference. The skill documentation says its analysis does not replace professional assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious, reporting that its actions may go beyond study-video analysis, including unexpected activity in export-only mode.

Mitigation: Review the reported behavior and consider avoiding installation until you are comfortable with it, as advised by the security guidance.

Risk: The security summary reports account credential handling in remote requests and remote video analysis; the scan was partial and does not prove the skill safe.

Mitigation: Consider avoiding installation until you understand and are comfortable with the account, credential, and remote video-analysis behavior; do not treat the partial scan or separate no-findings scan as resolving these concerns.

## Reference(s):

- [Study analysis API reference](artifact/references/api_doc.md)
- [Skill introduction and demo](https://lifeemergence.com/sample.html)
- [ClawHub release 1.0.23](https://clawhub.ai/smyx-sunjinhui/skills/smyx-study-analysis)

## Skill Output:

**Output Type(s):** [Analysis reports, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON or text reports; history listings can be presented as Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts local video files or video URLs; local video files are limited to 10 MB per skill documentation.]

## Skill Version(s):

1.0.23 (source: server-resolved release evidence; bundled SKILL.md states 1.0.26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
