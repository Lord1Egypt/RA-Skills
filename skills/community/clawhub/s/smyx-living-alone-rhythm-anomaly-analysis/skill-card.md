## Description:

Analyzes overnight bedroom or living-room video to estimate lights-off time and early-morning movement, compare them with a 7–14 day personal baseline, and report possible sleep-rhythm anomalies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Family members and community care workers use it to review a person living alone’s overnight routine and follow up when changes from their baseline suggest a need to check in. It reports visual routine indicators and does not provide medical diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overnight camera footage is highly sensitive, and the security assessment rates this release suspicious, citing video handling, account and credential activity, and behavior that may continue despite export-only options; the scan was partial.

Mitigation: Obtain informed consent and limit footage exposure; review upload destinations, HTTP configuration, account registration, and export-only behavior before installation or use with real footage or credentials.

Risk: A change in sleep timing or overnight movement can be mistaken for a health problem.

Mitigation: Treat alerts as prompts for a personal check-in, consider ordinary causes and repeated patterns, and do not use the report as a medical diagnosis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-living-alone-rhythm-anomaly-analysis)
- [Skill introduction](https://lifeemergence.com/sample.html)
- [API reference](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON analysis with Markdown summaries and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include lights-off time, early-morning activity metrics, baseline comparisons, anomaly categories, and follow-up suggestions; no medical diagnosis.]

## Skill Version(s):

1.0.16 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
