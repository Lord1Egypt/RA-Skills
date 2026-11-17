## Description:

Analyzes pet racing videos to identify start times, finish order, lane assignments, and possible false starts or lane crossings, and produces referee-support reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Race officials and event operators use the skill to review local race videos or video URLs for start timing, finish order, lane assignment, and possible racing fouls. Its reports support officiating; the source says final decisions remain with the on-site chief referee.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags credential and account/profile handling that is not clearly aligned with race-video judging.

Mitigation: Follow the security guidance and avoid installation until the maintainer explains why this handling is needed and how credentials and identity data are protected from external destinations.

Risk: The security evidence flags remote video processing without clear disclosure and says it is unclear when local video is uploaded.

Mitigation: Before use, obtain a clear explanation of when local video is uploaded and which external services receive video or related data.

Risk: The security scan is partial because a referenced local path was missing, so its evidence is incomplete.

Mitigation: Resolve the missing path and complete a security review before relying on the scan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-race-foul-detection-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API reference](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured JSON analysis reports; historical report lists are formatted as Markdown tables with report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include start times, finish order, lane assignments, possible foul findings, evidence clip locations, and report links; results are referee support.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
