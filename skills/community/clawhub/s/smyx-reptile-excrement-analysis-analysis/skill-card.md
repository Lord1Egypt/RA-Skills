## Description:

Analyzes reptile enclosure images or video frames for urate size and feces appearance, returning an assessment and suggested next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Reptile keepers and enclosure operators use this skill to assess urate and feces from enclosure images or video frames, review historical reports, and identify observations that may warrant veterinary attention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enclosure images, video, or URLs are sent to an external analysis service.

Mitigation: Use only with media you are comfortable sharing and review the service's data handling before installation.

Risk: The skill creates or reuses a local identity and retains service tokens and report history.

Mitigation: Review local token and report retention; consider a dedicated test identity and workspace.

Risk: Image quality or misleading visual signals can make health assessments unreliable.

Mitigation: Use clear, well-lit images and consult a reptile veterinarian for abnormal findings rather than treating the assessment as a diagnosis.

## Reference(s):

- [Reptile excrement analysis API reference](references/api_doc.md)
- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-reptile-excrement-analysis-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [JSON analysis reports or Markdown summaries and history tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include alert levels, recommended actions, and links to reports.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
