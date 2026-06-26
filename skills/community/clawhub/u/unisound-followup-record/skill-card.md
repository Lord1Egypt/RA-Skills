## Description: <br>
Structures Chinese outpatient follow-up medical records into detailed field outputs for history, examination, diagnosis, and treatment advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and clinical workflow teams use this skill to convert Chinese outpatient follow-up record text or supported document files into normalized medical-field outputs. It is intended for extraction and structuring, not clinical diagnosis or treatment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical record text may be sent to the configured remote LLM service, while the artifact's stated de-identification protection is not implemented in code. <br>
Mitigation: Verify the provider, endpoint, retention terms, and compliance posture before use; submit only already de-identified records. <br>
Risk: Prepared input or output files can be saved when users pass output paths or --save-prepared. <br>
Mitigation: Use controlled, secured destinations for saved files and avoid persistence options unless storage is approved for the data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-followup-record) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Example input record](artifact/example/gen_records.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [UTF-8 text with one extracted field per line, plus command-line usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an app key for a configured remote medical LLM endpoint; unsupported or missing fields are represented as "未提及".] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
