## Description:

Analyzes submitted video of an older adult's medication routine to identify pick-up, hand-to-mouth, and apparent swallowing steps and return a compliance result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and elder-care providers can use it to review a submitted medication-routine video and see which key steps were observed. Treat the result as an aid for follow-up and verify missed or uncertain steps with the person; it does not provide medical advice or replace a clinician.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags concerns about credential handling, account setup, destination checks, and whether a no-analysis option is honored.

Mitigation: Review credential and account behavior, confirm the analysis destination, and verify that analysis can be declined before use.

Risk: Medication videos contain sensitive health and personal information.

Mitigation: Obtain informed consent before sharing video and protect access to recordings and reports.

Risk: The security review describes submitted-video analysis and says not to rely on it for continuous monitoring or caregiver alerts; visual steps may also be uncertain.

Mitigation: Use results as an aid, not as proof of medication ingestion or a substitute for monitoring; manually confirm missed or uncertain steps.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-elderly-medication-compliance-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured medication-step analysis report; history results can be presented as a Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include observed steps, compliance status, timestamps, confidence, snapshot or report links, and an alert message.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata; packaged skill frontmatter states 1.0.22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
