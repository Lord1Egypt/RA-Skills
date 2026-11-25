## Description:

Analyzes fixed-camera reptile enclosure video to summarize hourly activity and compare observed patterns with the species' day and night rhythm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Reptile keepers and breeders can use enclosure video to review hourly activity patterns, identify possible changes in day and night activity, and receive a structured report for follow-up. The report is an activity analysis, not a veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports undeclared account creation, identity and token storage, and remote data handling that do not fit the advertised activity-monitoring purpose.

Mitigation: Avoid installing or using the skill until its publisher explains why these capabilities are needed and how account, credential, and video data are handled.

Risk: The assessment says scanner coverage is partial because a referenced local path was missing, so it does not establish that all artifact behavior was assessed; the export-only option is also unclear.

Mitigation: Review the missing component and clarify the export-only behavior before relying on the skill.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-reptile-circadian-activity-analysis)
- [API documentation](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [JSON, Text, Report links]

**Output Format:** [Structured analysis results and report links printed as text; historical report results are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Activity summaries may include hourly patterns, rhythm comparisons, alerts, and suggested follow-up.]

## Skill Version(s):

1.0.17 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
