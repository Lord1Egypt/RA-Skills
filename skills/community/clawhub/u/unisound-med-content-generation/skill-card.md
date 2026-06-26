## Description: <br>
医学科普、文档摘要、术语释义、教学案例与诊疗文书辅助生成。通过 --task 选择类型；仅含 `scripts/run.py`，可独立拷贝部署。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and medical content teams use this skill to send medical questions or source documents to a configured medical LLM for plain-language explanations, popular science content, clinical summaries, teaching cases, and draft clinical documentation. Outputs are auxiliary material and are not a substitute for clinical judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical prompts and source documents are sent to the configured medical LLM API. <br>
Mitigation: Use only approved endpoints and keys, and submit patient information only after de-identification and organizational approval. <br>
Risk: Generated medical explanations, summaries, teaching cases, or draft documentation may be incomplete or clinically incorrect. <br>
Mitigation: Treat outputs as auxiliary material and require qualified clinical review before use in care, documentation, or patient-facing communication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-med-content-generation) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/unisound-llm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Markdown, Shell commands, Configuration] <br>
**Output Format:** [JSON by default, text-only answer output when requested, and NDJSON for batch results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports task selection, JSON/JSONL/text/stdin inputs, dry-run parsing, output files, and configurable API URL, model, temperature, timeout, and system prompt.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
