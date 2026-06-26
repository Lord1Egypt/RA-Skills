## Description: <br>
Generates structured thematic research reports for events, policies, trends, and cross-industry investment topics from a natural-language query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to request thematic research or deep-dive reports on policies, events, trends, and cross-industry topics. It returns report text, sharing information, and local document attachments when the Eastmoney service provides them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Eastmoney EM_API_KEY and sends research queries to Eastmoney. <br>
Mitigation: Install only when that credential use and external service interaction are acceptable, and keep the API key out of prompts, logs, and generated files. <br>
Risk: The advertised no-save option is inconsistent with the implementation and may still write returned documents locally. <br>
Mitigation: Do not rely on --no-save to prevent file writes until fixed; inspect the configured output directory after use. <br>
Risk: Generated DOCX/PDF reports are external files produced by a third-party service. <br>
Mitigation: Treat generated documents as untrusted external files and review them before opening, sharing, or relying on their contents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/topic-research-report) <br>
- [Eastmoney Miaoxiang service](https://ai.eastmoney.com/mxClaw) <br>
- [Eastmoney thematic research API endpoint](https://ai-saas.eastmoney.com/proxy/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [Markdown report text with title, share URL, and optional DOCX/PDF attachment paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EM_API_KEY and may create local DOCX/PDF files returned by the Eastmoney service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
