## Description: <br>
Automatically parses PDF, TXT, and Markdown research reports to extract key viewpoints, data, investment advice, risks, and summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangq0687](https://clawhub.ai/user/zhangq0687) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to process individual or batches of research reports, extract structured insights with a local Ollama model, and save the results as JSON for later review or knowledge-base use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Report text is sent to the configured local Ollama service for extraction, which can expose confidential report content depending on local deployment, logging, and access controls. <br>
Mitigation: Use only trusted local Ollama deployments, review logging and access controls, and avoid processing confidential reports unless retention and cleanup expectations are understood. <br>
Risk: Extracted report summaries and model responses are saved as JSON files under the user's home directory. <br>
Mitigation: Review output files for sensitive content and apply local file retention, permissions, and cleanup policies appropriate to the reports being processed. <br>


## Reference(s): <br>
- [ClawHub Report Processor page](https://clawhub.ai/zhangq0687/report-processor) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/scripts/report_processor.py](artifact/scripts/report_processor.py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files, JSON] <br>
**Output Format:** [Markdown guidance with command examples and JSON report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves extracted report data under ~/.openclaw/workspace/data/reports/ and truncates model input and stored raw responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
