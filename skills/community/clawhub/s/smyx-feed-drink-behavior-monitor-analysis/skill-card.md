## Description:

Analyzes fixed-camera videos of feeders and waterers to quantify livestock feeding duration, feeding bouts and drinking frequency, comparing them against individual baselines to raise behavior anomaly alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

External users and farm operations teams use this skill to analyze fixed-camera feeder or waterer media, producing behavior statistics, baseline comparisons, anomaly levels, and report links for livestock feeding and drinking monitoring. It is not a disease diagnosis or treatment tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local camera media may be uploaded to a cloud analysis service.

Mitigation: Run only with approved media and approved service endpoints, and avoid submitting footage outside the intended feeder or waterer monitoring scope.

Risk: Bundled configuration includes development or plaintext HTTP endpoints alongside HTTPS endpoints.

Mitigation: Confirm the skill is configured for trusted HTTPS production endpoints before installation or execution.

Risk: Automatically managed identity and reusable service tokens can tie report history to a workspace.

Mitigation: Use an approved workspace identity, restrict access to local workspace data, and rotate or clear stored tokens according to policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-feed-drink-behavior-monitor-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Structured text or JSON analysis results; historical report lists may be returned as Markdown tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include feeding duration, feeding and drinking frequency, behavior timing, anomaly level, and a report export link.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact frontmatter is 1.0.9)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
