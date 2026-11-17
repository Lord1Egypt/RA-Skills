## Description:

Analyzes litter-box video to track cats’ visits, compare visit frequency and duration with historical baselines, and flag behavior changes for veterinary follow-up; it does not diagnose illness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Cat owners and care teams can use litter-area video to summarize each cat’s visit frequency and duration, compare behavior with historical patterns, and identify changes to discuss with a veterinarian. The results are behavioral alerts, not a medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the release suspicious, citing account and credential handling, remote account creation, and video uploads that are not clearly disclosed or aligned with the advertised analysis.

Mitigation: Review identity and credential handling, possible secret transmission, and what video data is processed externally before installing.

Risk: The scan was partial because a referenced path was missing, so the available evidence does not establish that all behavior was covered.

Mitigation: Review the missing path and complete a scan of the full release before relying on the security assessment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-litter-box-usage-monitor-analysis)
- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Structured analysis report with visit statistics, behavior alerts, suggestions, and report links; historical report lists are presented as Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Behavioral indicators only; not a veterinary diagnosis.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
