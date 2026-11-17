## Description:

Provides primary-care common disease decision support from patient symptoms, signs, and history, returning differential diagnoses, recommended exams, initial treatment advice, referral guidance, JSON, and a natural-language summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Community clinic and primary-care clinicians use this skill to draft common-disease triage and treatment-support guidance from patient-provided clinical text. The output is decision support that requires clinician review before use with patients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive patient information may be sent to a remote model, while the skill package claims de-identification that is not performed by the code.

Mitigation: Use only de-identified minimum-necessary clinical text unless local de-identification is added and the remote endpoint's data handling is approved.

Risk: Generated diagnoses, medication doses, and referral recommendations can be incorrect or incomplete.

Mitigation: Treat all outputs as untrusted clinical decision support and require review by a licensed clinician before patient care decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-common-disease-advice)
- [Configured remote medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON plus a natural-language summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print to stdout or write the same output to a user-specified file.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
