## Description:

Analyzes frontal images or short videos of older adults for facial asymmetry and mouth-corner deviation, returning non-diagnostic screening results and risk guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and elder-care teams use the skill to review facial asymmetry in images or videos and retrieve prior screening reports, prompting timely medical attention when concerning changes appear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Elderly face images, videos, and report history are sent to configured cloud services.

Mitigation: Obtain consent from the person or caregiver and review the destination service before sharing sensitive media or reports.

Risk: Screening results could be mistaken for a medical diagnosis or delay urgent care.

Mitigation: Treat the results as non-diagnostic; seek immediate medical attention if stroke symptoms are suspected.

Risk: The skill can create or reuse a backend identity and retain its tokens in a local workspace database.

Mitigation: Review or clear the workspace data database if persistent identity tokens are not desired.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/smyx-sunjinhui/skills/smyx-elderly-facial-asymmetry-analysis)
- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes asymmetry measures, risk-level prompts, and links to reports; historical report listings are available.]

## Skill Version(s):

1.0.12 (source: server-resolved ClawHub release; bundled SKILL.md states 1.0.18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
