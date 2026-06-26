## Description: <br>
Assists primary care clinicians by taking diagnoses and patient medication context, recommending drug plans, checking interactions and contraindications, and returning dosage guidance as JSON plus a natural language summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External primary care clinicians use this skill to prepare prescription assistance notes from diagnosis, renal function, allergy history, and concurrent medication details. The output is decision support and does not replace physician or pharmacist review before a prescription is issued. <br>

### Deployment Geography for Use: <br>
Global, subject to local healthcare practice, prescription, consent, and data protection requirements. <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive prescription and patient details are sent to a configured remote medical model service. <br>
Mitigation: Use only the minimum necessary patient information, remove direct identifiers before use, and require documented consent, retention, and approved endpoint controls before processing protected health information. <br>
Risk: The artifact claims de-identification, but the security evidence says the code does not perform it. <br>
Mitigation: Perform de-identification outside the skill or add verified de-identification controls before relying on privacy claims. <br>
Risk: Prescription recommendations may be incorrect, incomplete, or unsuitable for a specific patient. <br>
Mitigation: Require review and approval by a licensed clinician or pharmacist before issuing any prescription. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-prescription-assist) <br>
- [Publisher profile: unisound-llm](https://clawhub.ai/user/unisound-llm) <br>
- [Configured medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON followed by a natural language summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print to stdout or write an output file; uses a remote medical model API and an app key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
