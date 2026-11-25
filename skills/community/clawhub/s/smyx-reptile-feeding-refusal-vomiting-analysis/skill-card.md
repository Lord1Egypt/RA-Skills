## Description:

Analyzes reptile feeding videos to identify prey attacks, swallowing, feeding refusal, and regurgitation, then produces event reports and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Reptile keepers and enclosure operators can use feeding-period video to record feeding behavior, review possible refusal or regurgitation events, and view related alerts and historical reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with high confidence, citing credential and identity handling and capabilities that may not match the reptile-video analysis purpose.

Mitigation: Before installation, verify the remote service and credential handling, and confirm that identity persistence and account registration are acceptable.

Risk: The security review notes remote media processing with limited disclosure.

Mitigation: Understand when video is uploaded and what processing the remote service performs before submitting footage.

Risk: Scanner coverage is partial because a local reference in the skill description was missing, so the security evidence is incomplete.

Mitigation: Review the missing reference and reassess the skill before installation.

## Reference(s):

- [Skill release page](https://clawhub.ai/18072937735/skills/smyx-reptile-feeding-refusal-vomiting-analysis)
- [API reference](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Structured feeding-event analysis and historical reports, with alerts, recommendations, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes observed attack, swallowing, refusal, and regurgitation indicators with confidence and context fields when available.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
