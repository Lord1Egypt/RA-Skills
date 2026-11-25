## Description:

Analyzes pet camera or feeder images and videos for everyday health behaviors and produces structured monitoring reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners use the skill to review camera or feeder footage for changes in eating, drinking, elimination, demeanor, vomiting, or limping, and to view prior monitoring reports. Its findings are for reference and do not replace veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the skill suspicious, reporting undisclosed account and token handling, persistent local user data, and possible media analysis or uploads even in export-only mode; the scan was partial because a referenced local path was missing.

Mitigation: Review account, token, and local data handling and confirm whether media is uploaded before use. Do not treat export-only mode as a privacy guarantee; resolve the missing path and complete a security review.

Risk: Pet behavior analysis may be mistaken for a veterinary diagnosis.

Mitigation: Treat reports as informational; consult a veterinarian about health concerns or detected abnormalities.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-pet-health-monitoring-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API reference](references/api_doc.md)
- [Analysis API errors](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Structured health monitoring report in JSON or text, with Markdown report listings and report links when querying history]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include behavior observations, health indicators, alerts, suggestions, and links to reports; results are not veterinary diagnoses.]

## Skill Version(s):

1.0.22 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
