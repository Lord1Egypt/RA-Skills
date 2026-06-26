## Description: <br>
A management skill for solo Traditional Chinese Medicine practitioners that manages patient records, medical charts, herbal inventory, appointments, billing, financial reports, and local Excel data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slamw](https://clawhub.ai/user/slamw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External solo TCM practitioners use this skill for day-to-day clinic operations, including registering patients, recording visit notes and prescriptions, managing herbal stock, scheduling appointments, and summarizing billing or income. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive patient, medical, appointment, and payment records in local Excel files without built-in privacy controls. <br>
Mitigation: Use only in a controlled local directory with appropriate consent, access controls, encryption, protected backups, retention and deletion procedures, and applicable healthcare privacy compliance. <br>
Risk: Record, billing, appointment, and inventory actions can write or modify operational clinic data. <br>
Mitigation: Require explicit user confirmation before executing any command that creates or changes records, charges, appointments, or inventory quantities. <br>
Risk: Medical-chart and prescription workflows can capture clinical content that may be mistaken for independent medical advice. <br>
Mitigation: Use the skill as a recordkeeping and workflow aid for qualified practitioners, and keep clinical responsibility with the practitioner. <br>


## Reference(s): <br>
- [TCM Clinic Data Table Schema Reference](references/data-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown summaries and tables, shell command invocations, and local Excel workbook files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses python3 and openpyxl; writes clinic data to local .xlsx files under clinic_data/.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
