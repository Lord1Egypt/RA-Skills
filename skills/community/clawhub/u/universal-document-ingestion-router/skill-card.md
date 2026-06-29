## Description: <br>
Document parsing and knowledge-base import router. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollis9087](https://clawhub.ai/user/hollis9087) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to classify local document files, route them to available parsers, and prepare standardized outputs for downstream knowledge-base ingestion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-selected local documents and writes parsed outputs that may contain sensitive source content. <br>
Mitigation: Use narrow input directories, choose output locations carefully, and avoid --copy-sources for confidential material unless retained source copies are intentional. <br>
Risk: Poor extraction quality, especially OCR failures or unsupported formats, can produce incomplete material for downstream knowledge bases. <br>
Mitigation: Review document status and quality warnings such as blocked_or_failed, empty_extraction, and no_parser_succeeded before indexing parsed outputs. <br>
Risk: Batch mode can copy source files into the output tree when --copy-sources is enabled. <br>
Mitigation: Enable --copy-sources only for intended test or retention workflows and keep the output directory within the expected data handling boundary. <br>


## Reference(s): <br>
- [Architecture](references/architecture.md) <br>
- [Development Report](references/development-report.md) <br>
- [Agent Integration Notes](references/agent-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON files, JSON stdout, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates document.json for parse attempts, document.md when extraction succeeds, chunks.jsonl when chunking is enabled, tables/ for reliable table extraction, and batch_summary.json for batch mode.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
