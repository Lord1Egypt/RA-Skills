## Description:

Analyzes newborn facial images for visual jaundice indicators and returns a preliminary risk hint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and healthcare staff can use the skill to screen newborn facial images for possible jaundice and review a preliminary risk hint with suggested next steps. Its visual output is for screening and does not replace clinical assessment or bilirubin testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with high confidence, citing undeclared account and history access, credential handling, and risks involving sensitive newborn media and identity data; its scan is incomplete because a referenced local path was missing.

Mitigation: Clarify account, credential, and data-transfer behavior and review the missing component before installation; avoid submitting credentials or sensitive images until those behaviors are understood.

Risk: Newborn facial images and identity data are highly sensitive.

Mitigation: Obtain a guardian's informed consent and confirm appropriate access, storage, and transfer protections before uploading images or using cloud reports.

Risk: Visual estimates can be misleading and are not a clinical bilirubin measurement.

Mitigation: Treat results as preliminary screening only; seek clinician assessment and confirm concerns with transcutaneous or serum bilirubin testing.

## Reference(s):

- [API Reference](references/api_doc.md)
- [Skill listing](https://clawhub.ai/18072937735/skills/smyx-neonatal-jaundice-screening-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis report with a risk hint, observations, and recommended next steps; historical reports can be listed in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual screening only; a clinician and bilirubin testing should confirm concerns. Poor lighting or an obscured face may make results inconclusive.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
