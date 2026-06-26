## Description: <br>
Converts Word, Excel, or PDF clinical CRF and protocol documents into REDCap-compatible data dictionary CSV files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenlcj](https://clawhub.ai/user/kenlcj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical research teams and REDCap builders use this skill to turn CRF, protocol, questionnaire, or survey documents into import-ready REDCap data dictionaries. It is intended for workflows where users can review the generated CSV before importing it into a study. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical-derived CSV files may contain sensitive study or patient-related information, and the artifact instructs users to share CSV output through Feishu without clear consent, recipient, or privacy controls. <br>
Mitigation: Use de-identified test documents unless sharing and output handling are explicitly approved; avoid Feishu sharing when controls are unclear. <br>
Risk: Generated REDCap dictionaries can misrepresent clinical fields, validation rules, identifiers, or branching logic if the source document is complex or ambiguous. <br>
Mitigation: Manually validate the generated CSV, including identifier flags and REDCap import behavior, before using it in a study. <br>


## Reference(s): <br>
- [ClawHub skill homepage](https://clawhub.ai/skills/redcap-crf-generator) <br>
- [Published skill page](https://clawhub.ai/kenlcj/redcap-crf-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [CSV REDCap data dictionary with Markdown or terminal guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write UTF-8 CSV files for REDCap import and show preview output for review.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence; artifact metadata reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
