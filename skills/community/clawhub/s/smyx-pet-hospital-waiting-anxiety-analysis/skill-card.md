## Description:

Triggers when a user provides a pet hospital waiting area video URL or file for analysis; supports local video uploads or network URLs to call server-side APIs for anxiety-related behavior recognition, detecting open-mouth panting intensity, limb/torso trembling amplitude, ear-flattening degree and other stress signals, outputting a standardized anxiety level (1-5) to help medical staff identify high-stress pets and prioritize care or comfort (without diagnosing diseases or prescribing treatment).

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Veterinary clinic staff and pet care teams can use the skill to review waiting-area pet videos, summarize visible stress-related behaviors, and prioritize comfort or attention for animals with higher estimated anxiety. The estimate is for workflow support and does not diagnose disease or prescribe treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags credential exposure and privacy concerns for submitted video and service access.

Mitigation: Avoid sending sensitive footage or credentials unless you have independently verified how the service handles them.

Risk: The security summary reports behavior beyond the stated purpose and scope concerns.

Mitigation: Review the service and requested access before use, and provide only footage needed for the requested assessment.

Risk: Individual traits and recording conditions can affect the estimated anxiety level.

Mitigation: Treat the result as a workflow aid and combine it with direct observation; do not use it as a diagnosis or treatment recommendation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-pet-hospital-waiting-anxiety-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API reference](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Structured anxiety assessment report; history results can be presented as a Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports an estimated anxiety level from 1 to 5 and observed behavior signals; not a medical diagnosis or treatment plan.]

## Skill Version(s):

1.0.21 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
