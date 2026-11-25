## Description:

Analyzes medication-area video for pickup, hand-to-mouth, and apparent swallowing steps, then reports an observed medication-compliance status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Older adults’ caregivers and care staff can submit a medication-area video to review whether pickup, hand-to-mouth, and apparent swallowing steps were observed. The result is an aid for confirming observed actions and does not provide medical advice or a medication plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medication videos contain sensitive health information, and the documented workflow submits them for remote analysis with automatic account handling.

Mitigation: Obtain informed consent, confirm the service’s video and report handling and account setup, and protect stored footage and reports.

Risk: The security assessment reports a mismatch between advertised continuous monitoring and the video submission workflow, and advises against relying on continuous monitoring or caregiver alerts unless confirmed.

Mitigation: Treat results as video-based observations; independently confirm any monitoring or alert capability and manually check uncertain or incomplete results.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-elderly-medication-compliance-analysis)
- [API interface notes](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Text]

**Output Format:** [Structured analysis results and Markdown report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include observed step statuses, compliance status, confidence, timestamps, reminders, and report links when returned by the service.]

## Skill Version(s):

1.0.18 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
