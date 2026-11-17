## Description:

Detects morbid behavioral cues in poultry and pigs from continuous barn videos — such as difficulty standing, ruffled feathers/piloerection, isolation, drowsiness and appetite loss — and outputs behavior type with risk level up to 2-3 days ahead of visible clinical signs. | 识别站立困难、羽毛蓬松、离群、嗜睡等病态行为，比人工观察提前2-3天。

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Livestock operators and farm teams can screen poultry or pig barn images and videos for unusual behavior, review risk levels and affected locations, and query prior reports. Results support early screening and do not provide a veterinary diagnosis or treatment recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks this release suspicious and incomplete, citing reported account and credential handling, unexpected remote and file activity, and video uploads that do not match the stated behavior-screening purpose.

Mitigation: Review these behaviors before installing; avoid providing credentials or sensitive footage until the findings are understood.

Risk: Barn images and videos are sent to a remote analysis service, which may expose sensitive farm or bystander information.

Mitigation: Use only footage approved for remote processing and remove unrelated sensitive content where practical.

Risk: Behavior screening can be mistaken for a veterinary diagnosis or treatment recommendation.

Mitigation: Treat results as an early screening aid and consult a veterinarian for diagnosis or treatment decisions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-sick-poultry-behavior-detect-analysis)
- [API reference](references/api_doc.md)
- [Skill introduction and demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON]

**Output Format:** [Structured behavior screening report with behavior observations, risk level, affected locations and group statistics; historical report lists use a Markdown table with links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts image or video input. Screening results are for reference and are not a disease diagnosis or treatment advice.]

## Skill Version(s):

1.0.12 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
