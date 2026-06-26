## Description: <br>
A management skill for solo Traditional Chinese Medicine practitioners that handles patient records, medical charts, herbal inventory, appointments, and clinic financial bookkeeping in local Excel files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slamw](https://clawhub.ai/user/slamw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Solo TCM practitioners and clinic operators use this skill to create and search patient files, record consultations and prescriptions, manage herbal inventory, schedule appointments, and summarize clinic finances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive patient, medical, appointment, and financial records in plaintext Excel files. <br>
Mitigation: Use only on a trusted, access-controlled device with encryption, secure backups, retention rules, and any required healthcare compliance review. <br>
Risk: Patient details can be printed in terminal output, logs, or shared agent transcripts. <br>
Mitigation: Avoid running the skill in shared terminals or logging environments when using real patient data. <br>


## Reference(s): <br>
- [Data schema reference](references/data-schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/slamw/tcm-clinic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and summaries with optional shell commands that call a local Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local Excel workbooks under clinic_data/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
