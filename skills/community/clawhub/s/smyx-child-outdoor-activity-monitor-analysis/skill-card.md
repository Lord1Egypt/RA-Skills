## Description:

This skill uses fixed-camera footage at a home entrance or balcony to track a child's indoor and outdoor crossings, estimate daily outdoor time, and generate duration summaries and reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers use the skill to review a child's estimated outdoor time from home entrance or balcony camera footage and receive duration reminders. Developers can integrate the reports into family health or education applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the skill suspicious because its reported behavior includes sensitive video handling and remote account activity, with a mismatch between the stated monitoring purpose and some reported capabilities.

Mitigation: Review the skill before use, verify the remote service and what identity and video data it receives, and run analysis only with explicit intent.

Risk: Home camera footage contains sensitive information about children.

Mitigation: Obtain a guardian's informed consent and encrypt and safeguard the footage.

Risk: The security scan was partial because a referenced local path was missing, so its findings do not cover every possible dependency or runtime behavior.

Mitigation: Review the available files and verify dependencies and runtime behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-child-outdoor-activity-monitor-analysis)
- [API documentation](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured activity reports and Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include crossing events, session durations, daily totals, recommendation progress, reminders, and report links. Counts reflect observed crossings and may not represent actual exercise.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
