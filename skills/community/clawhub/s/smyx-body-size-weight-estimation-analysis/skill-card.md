## Description:

Estimates livestock body length and body weight from side-view videos or frames, tracking fattening progress in a contactless manner. | 通过视频视觉估测体长、体重，追踪育肥进度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Livestock producers and operations teams can use side-view images or videos to estimate an animal’s body dimensions, weight, and fattening stage, and to review historical estimation reports. The estimates are intended as progress references rather than feeding or sale recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with high confidence, citing account and credential handling, remote actions, and side effects beyond the stated livestock-estimation purpose.

Mitigation: Consider not installing until the publisher explains the account, credential, upload, and remote-action behavior and how user data is protected. The scan was partial, so the available evidence does not establish that every referenced component was reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-body-size-weight-estimation-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API reference](artifact/references/api_doc.md)
- [Analysis API reference](artifact/skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown]

**Output Format:** [Structured estimation report; historical reports are presented as a Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include estimated body length, height, girth or width, weight, fattening stage, confidence or usability notes, and report links.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
