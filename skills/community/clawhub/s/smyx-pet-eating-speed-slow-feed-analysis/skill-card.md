## Description:

Analyzes pet food-bowl videos to estimate eating duration and speed, compare results with a safety threshold, and suggest slow-feeding interventions without diagnosing disease.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and pet-care teams use it to review feeding videos, estimate eating duration and speed, and receive non-diagnostic slow-feeding suggestions. Developers can connect the results to prompts or device-side slow-feeder interventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports credential and identity handling concerns, as well as behavior beyond the stated pet-feeding analysis purpose.

Mitigation: Review credential and identity handling and confirm the skill's behavior before installation or use.

Risk: ClawScan reports that video processing may occur when export-only mode is selected, and the scan is incomplete.

Mitigation: Confirm export-only behavior and how submitted videos are handled before providing pet videos; avoid installation until these points have been reviewed.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-pet-eating-speed-slow-feed-analysis)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured analysis report with eating timestamps, duration and speed estimates, threshold assessment, suggestions, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are health guidance only; the skill does not diagnose disease. Device-side interventions are based on the report.]

## Skill Version(s):

1.0.17 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
