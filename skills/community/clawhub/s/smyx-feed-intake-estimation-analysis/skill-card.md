## Description:

Estimates daily feed intake per livestock individual from continuous feeder videos by tracking the change of feed remaining in the trough, and outputs intake trend with anomaly alerts. | 通过食槽视频估算每日采食量变化，异常时预警。

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Livestock farm operators and feed management teams use this skill to estimate daily feed intake from feeder images or video, review intake trends, and receive anomaly alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the skill suspicious and reports concerns about video uploads, account and credential handling, external data transfers, and local data retention.

Mitigation: Before use, review where feeder videos are sent, how accounts and credentials are handled, and what data is retained locally; confirm these practices fit your data policies.

Risk: The security scan was partial because a referenced local path was missing, so it does not establish that all referenced material was reviewed.

Mitigation: Review the missing referenced material and complete the security review before installing or deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-feed-intake-estimation-analysis)
- [API documentation](references/api_doc.md)
- [Skill usage introduction](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured JSON analysis reports and Markdown report listings with report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily feed intake estimates, intake trends, anomaly alerts, and report links; basic, standard, and JSON detail levels.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
