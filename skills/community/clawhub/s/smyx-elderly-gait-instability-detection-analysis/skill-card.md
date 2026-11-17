## Description:

Analyzes straight-line walking videos to estimate gait measures and report a low, medium, or high fall-risk screening level.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and elder-care teams use walking videos to review estimated step length, gait speed, cadence, and trunk sway alongside fall-risk screening results. The reports support monitoring, not medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Elderly gait footage or video URLs are sent to a cloud service and may contain sensitive health information.

Mitigation: Obtain informed consent from the person or guardian before use and confirm the publisher's retention and access-control policy.

Risk: Analyses and report history are linked to a persistent internal identity, which may be unexpected to users.

Mitigation: Explain this linkage and request explicit confirmation before looking up report history or generating export links.

Risk: Fall-risk scores and estimated gait measurements could be mistaken for a diagnosis.

Mitigation: Present results as screening only and seek a qualified clinical assessment when medically relevant.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-elderly-gait-instability-detection-analysis)
- [Gait analysis API reference](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured gait report in Markdown or JSON, with screening results and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can display cloud-linked report history or save results to a file.]

## Skill Version(s):

1.0.12 (source: ClawHub release; bundled SKILL.md states 1.0.18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
