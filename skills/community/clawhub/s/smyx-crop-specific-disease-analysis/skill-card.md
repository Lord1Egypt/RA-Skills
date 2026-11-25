## Description:

Expands crop disease identification to cover economic-crop-specific diseases such as corn leaf blights, potato late blight, peanut leaf spot, and tomato viral disease.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Growers and agricultural users can submit crop leaf images or videos for visual identification of diseases affecting corn, potatoes, peanuts, and tomatoes. The skill returns a structured preliminary assessment with disease labels, confidence, and symptom descriptions; its documentation says it does not provide treatment recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with medium confidence, citing gaps between its crop-disease purpose and its account, video-analysis, and data-handling behavior.

Mitigation: Before installing, clarify the tool access, remote account creation, credential storage, and image/video/report data transfers; review the incomplete API reference.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-crop-specific-disease-analysis)
- [Skill introduction demo](https://lifeemergence.com/sample.html)
- [API reference (incomplete)](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured disease analysis report with disease type, confidence, symptom description, and report link; history queries return report records as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image or video disease assessment; report history can be queried.]

## Skill Version(s):

1.0.19 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
