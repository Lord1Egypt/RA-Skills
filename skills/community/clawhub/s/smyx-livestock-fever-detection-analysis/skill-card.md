## Description:

Detects abnormal body temperature rises or drops in livestock and poultry from thermal or visible-light imagery, and provides fever or hypothermia alerts based on visual thermal features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Livestock producers and animal health teams can use thermal or visible-light images and videos to screen animals for possible temperature anomalies and review analysis reports. Results are for screening and do not provide disease diagnoses or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with high confidence, citing account, credential, and remote-service behavior beyond its stated temperature-analysis purpose, as well as safeguards that may not work as described. The scan was partial, and its findings do not establish malicious intent.

Mitigation: Before installing, verify that the account handling, data sent to the analysis service, and report-retrieval behavior meet your requirements.

## Reference(s):

- [API interface documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-livestock-fever-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured temperature-screening results and Markdown report lists with report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include individual locations, estimated temperature ranges, anomaly levels, and screening alerts; not a disease diagnosis.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
