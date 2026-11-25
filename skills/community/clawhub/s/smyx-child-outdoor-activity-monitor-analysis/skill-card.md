## Description:

Analyzes fixed-camera footage at a home or balcony entrance to estimate a child's daily outdoor time from exit and return events and report when it falls below a configured target.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and child-care teams can review doorway-camera footage for a child's exit and return events, daily outdoor-time estimates, and low-time reminders. The results are activity statistics rather than medical assessments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks this release suspicious, citing privacy-sensitive video uploads and account handling, behavior that does not clearly match the description, and partial scan coverage due to a missing referenced path.

Mitigation: Before installation, clarify the video destination, guardian consent and data protection, whether export-only behavior applies, and account and token creation and storage.

## Reference(s):

- [API reference](artifact/references/api_doc.md)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-child-outdoor-activity-monitor-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured activity report with event timestamps, duration estimates, and reminders; historical report lists can be presented as Markdown tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates are based on doorway exit and return events and do not establish actual exercise or medical status.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
