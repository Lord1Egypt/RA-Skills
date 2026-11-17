## Description:

Analyzes pet grooming area images or videos to estimate matting, shed hair volume, grooming effectiveness, and hairball risk, and can retrieve prior reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners, caregivers, and grooming teams can use this skill to review grooming area photos or videos, get an estimate of coat matting and shed hair, and view a grooming effectiveness and hairball risk report. It is intended for care reference, not medical diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the skill suspicious and reports credential and identity handling, persistent user data and report-history access, and behavior beyond the stated grooming analysis purpose; the scan was partial.

Mitigation: Review the skill and the security findings before installation, with attention to identity, credential, and persistent history handling.

Risk: Local grooming images and videos may be processed remotely, as noted in the security guidance.

Mitigation: Review the remote data handling and upload only media you are comfortable sharing for analysis.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-grooming-effectiveness-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis report in JSON or text, with historical reports presented as a Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hair and shed volume estimates are visual and approximate; results are for grooming reference and do not provide medical diagnosis or treatment.]

## Skill Version(s):

1.0.16 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
