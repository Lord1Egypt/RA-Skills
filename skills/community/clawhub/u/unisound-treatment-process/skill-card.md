## Description: <br>
Generates structured treatment-process summaries from course-of-illness records by sending de-identified clinical text to an internal medical language model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized clinical documentation users use this skill to turn de-identified inpatient course records into a structured treatment-process narrative for medical record filing, homepage completion, and case statistics. Generated text requires review by a licensed clinician before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive medical records and sends prepared text to a disclosed external medical LLM API. <br>
Mitigation: Install only in an authorized medical-data environment, use de-identified records, and approve the hivoice.cn endpoint and appkey before use. <br>
Risk: Generated clinical narratives may be incomplete or medically incorrect. <br>
Mitigation: Require review and sign-off by a licensed clinician before filing or downstream use. <br>
Risk: Debug or output flags can write prepared text or generated outputs to disk. <br>
Mitigation: Use output paths and --save-prepared only in secured directories and avoid saving sensitive prepared text unless needed for controlled debugging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-treatment-process) <br>
- [Unisound-LLM publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [hivoice.cn medical LLM API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [UTF-8 plain text printed to stdout, with optional text or JSON file output paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts JSON, text, PDF, Word, Excel, and CSV inputs after preprocessing; optional debug mode can save prepared text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
