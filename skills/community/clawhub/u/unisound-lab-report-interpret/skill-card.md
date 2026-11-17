## Description:

Interprets basic laboratory and diagnostic report text, identifies abnormal indicators, and returns clinical significance plus follow-up suggestions as JSON and a natural-language summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Community clinic and primary care clinicians use this skill to get auxiliary interpretations of blood, biochemical, urine, coagulation, thyroid, and ECG report text. Its output is for clinician review and should not be treated as a final diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may contain patient identifiers or sensitive clinical data that are sent to the configured model endpoint.

Mitigation: Manually de-identify reports before use and review endpoint trust before sending real patient data.

Risk: Generated interpretations may be incomplete, incorrect, or unsuitable for diagnosis.

Mitigation: Require clinician review before using results for patient care or follow-up decisions.

Risk: Saving outputs to disk can persist sensitive interpretations outside the agent session.

Mitigation: Use secure output locations and apply local retention and access controls for generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-lab-report-interpret)

## Skill Output:

**Output Type(s):** [text, json, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON plus natural-language summary in Markdown or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write interpreted results to a user-selected output file.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
