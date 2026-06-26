## Description: <br>
Normalizes URLs, PDFs, Word, Excel, CSV, images, and text into clean JSON for reliable, universal input parsing in under 2 seconds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etytabs](https://clawhub.ai/user/etytabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to normalize URLs, documents, spreadsheets, images, and text into deterministic JSON before passing content to LLM agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote HTTP or SDK usage may send selected files, URLs, and parsed output to Reversal's service. <br>
Mitigation: Use the local stdio setup for confidential, internal, regulated, or proprietary inputs; review service terms before remote use. <br>
Risk: Remote mode and image parsing can involve sensitive API credentials. <br>
Mitigation: Store keys in the agent host's secret or environment configuration, avoid logging them, and do not commit them to source control. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/etytabs/reversal-engine) <br>
- [Reversal repository listed in artifact](https://github.com/Etytabs/REVERSAL) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code, JSON] <br>
**Output Format:** [Markdown guidance with JSON, bash, TOML, Python, and TypeScript examples; the integration outputs structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote HTTP and SDK use can require API keys; image and dashboard screenshot parsing may require ANTHROPIC_API_KEY; batch parsing supports up to 10 sources.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
