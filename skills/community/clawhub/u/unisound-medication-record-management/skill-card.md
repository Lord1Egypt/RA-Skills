## Description: <br>
Manages patient medication records by normalizing medication entries, organizing active and stopped medications, and producing a structured history summary with Markdown analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to capture, update, query, import, and export long-term medication records. It is intended for record management and summaries, not for changing treatment plans or replacing clinician guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive medication records and extracted document text are sent to a remote model API. <br>
Mitigation: Use only with appropriate consent and privacy review, and avoid submitting data that should not leave the user's environment. <br>
Risk: The generated text may include medication interaction risk commentary that users could mistake for medical advice. <br>
Mitigation: Treat model-generated analysis as informational only and require clinician review for medication decisions. <br>
Risk: PDF, Office, and image inputs require parsers or OCR tools that increase exposure when processing untrusted files. <br>
Mitigation: Process untrusted documents in a sandboxed runtime and keep optional parsers and OCR dependencies patched. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/unisound-llm/unisound-medication-record-management) <br>
- [Unisound-LLM publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [MedTimer reference source](https://f-droid.org/en/packages/com.futsch1.medtimer/) <br>
- [HiVoice chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Analysis, Files] <br>
**Output Format:** [UTF-8 JSON containing structured medication data and Markdown text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided app key and sends medication records to a remote model API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
