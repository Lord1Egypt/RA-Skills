## Description: <br>
Generates academic figures from PDF or plain-text papers, including architecture diagrams, flowcharts, motivation figures, result charts, captions, and PDF-to-text extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljk00000](https://clawhub.ai/user/ljk00000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, paper authors, and developers use this skill to extract paper text, scan for figure candidates, and generate academic diagrams or result charts with captions for publication drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paper content may be sent to configured external APIs for LLM and image generation. <br>
Mitigation: Use only papers and API providers approved for the data, and avoid confidential content unless the provider and policy allow it. <br>
Risk: The Matplotlib result-chart path can execute generated Python code locally. <br>
Mitigation: Inspect generated Python before execution and run the skill in a restricted virtual environment or sandbox. <br>
Risk: API keys passed on the command line can be exposed through shell history or process listings. <br>
Mitigation: Prefer environment variables or OpenClaw configuration for credentials, and avoid command-line secrets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ljk00000/ynu-papergraphgeneration-qclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, configuration] <br>
**Output Format:** [Generated image files, captions, Mermaid topology text, Matplotlib Python code, and PDF-extracted plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python plus configured API URL and API key environment variables; paper content may be sent to the configured API provider.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
