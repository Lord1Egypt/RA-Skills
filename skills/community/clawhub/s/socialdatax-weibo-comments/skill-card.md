## Description:

Analyzes Weibo comments and replies to surface audience feedback, sentiment themes, objections, pain points, FAQs, and discussion summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Social media analysts and content teams use this skill to review Weibo post comments and replies, identify recurring audience themes, objections, pain points, and FAQs, and prepare discussion summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary marks the release suspicious because its CLI examples use a changeable latest package; the scan was partial, and a changed or compromised package could run with local permissions and access credentials.

Mitigation: Review the package and release before execution, use a reviewed fixed version where possible, and provide only the permissions and credentials needed for the task.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-weibo-comments)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text]

**Output Format:** [Structured comment and reply data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pagination may return one or multiple pages; an empty comment set can be a valid result.]

## Skill Version(s):

0.1.24 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
