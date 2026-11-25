## Description:

Estimates livestock body length and body weight from side-view videos or frames, tracking fattening progress in a contactless manner. | 通过视频视觉估测体长、体重，追踪育肥进度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Livestock producers and farm operators use the skill to estimate body measurements, weight, and fattening stage from side-view images or videos, and to track growth without handling animals. Results are estimates for progress tracking and are not feeding or slaughter recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious with medium confidence, citing account and credential handling, remote requests, and behavior outside the stated livestock-estimation purpose; the scan is partial, so the evidence is incomplete and does not establish malicious intent.

Mitigation: Before installation, verify the publisher account and identity/token handling, confirm where local videos are sent, and review whether the export-only option and report lookup behave as intended.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-body-size-weight-estimation-analysis)
- [Livestock estimation API reference](artifact/references/api_doc.md)
- [API formats and error codes](artifact/skills/smyx_analysis/references/api_doc.md)
- [Skill introduction video](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured JSON analysis report; historical reports are presented as a Markdown table.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include estimated body length, height, chest girth, weight, fattening stage, confidence or usability notes, and a report link. Estimates are for reference.]

## Skill Version(s):

1.0.17 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
