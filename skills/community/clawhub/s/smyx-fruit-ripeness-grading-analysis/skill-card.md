## Description:

Analyzes tomato and strawberry images or videos to estimate fruit color, colored-area coverage, gloss, relative size, and ripeness stage, then returns a structured grading report and harvest guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Growers, greenhouse operators, fruit cooperatives, and home gardeners can use the skill to assess tomato or strawberry images and videos, classify fruit by ripeness stage, and support harvest timing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags substantial account and credential handling and network activity beyond the stated grading purpose.

Mitigation: Review the account behavior and required permissions before use, and restrict credentials to the minimum necessary until their use is understood.

Risk: Images or videos may be uploaded for analysis, and the security guidance calls for clarifying media handling.

Mitigation: Confirm the service destination and data handling before submitting media; use only images or videos you are authorized to share.

Risk: The security assessment notes analysis may run despite an export-only option.

Mitigation: Do not rely on export-only mode to avoid analysis until its behavior is verified; review the behavior before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fruit-ripeness-grading-analysis)
- [Skill usage demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON or Markdown report with ripeness grades, observations, and harvest guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes image or video inputs; reports fruit color, colored-area ratio, gloss, relative size, and ripeness stage. Results are visual estimates for harvest decisions.]

## Skill Version(s):

1.0.14 (source: evidence.json release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
