## Description: <br>
Refines SRT subtitle files by removing filler words, correcting ASR recognition errors, preserving timestamps, and sending the optimized subtitle file and token-use report through Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TrueTechLabs](https://clawhub.ai/user/TrueTechLabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to clean and correct SRT subtitle files while preserving subtitle indices and timestamps. It is suited for workflows that can send subtitle text to SiliconFlow for LLM processing and deliver results through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subtitle contents are sent to external services for LLM processing and Feishu delivery. <br>
Mitigation: Use only with subtitles approved for sharing with SiliconFlow and Feishu; avoid confidential, regulated, customer, or internal meeting transcripts unless an approved data-handling process is in place. <br>
Risk: The security evidence reports exposure of API keys and subtitle contents in logs. <br>
Mitigation: Redact credentials and subtitle text from logs, restrict log access, and rotate any API key that may have been exposed before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TrueTechLabs/subtitle-refiner) <br>
- [SiliconFlow Chat Completions API](https://api.siliconflow.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, API calls, Shell commands] <br>
**Output Format:** [SRT file plus Feishu delivery message and token-use summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes optimized subtitles under workspace/subtitle_refine with the original timing preserved.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
