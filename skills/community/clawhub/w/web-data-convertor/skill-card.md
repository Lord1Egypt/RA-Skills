## Description: <br>
Web Data Convertor converts JSON, CSV, XML, YAML, Markdown, HTML, query strings, and Unix timestamps through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert API, configuration, content, URL, and timestamp data between common web formats through AgentPMT-hosted calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversion inputs are sent to AgentPMT-hosted processing. <br>
Mitigation: Do not submit secrets, credentials, private configuration, regulated data, or sensitive personal data unless external processing by AgentPMT is approved. <br>
Risk: Converted Markdown or HTML may contain unsafe links or content if it is later rendered or published. <br>
Mitigation: Treat converted Markdown and HTML as untrusted content, and sanitize or validate links before publishing or rendering it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/web-data-convertor) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/web-data-convertor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration] <br>
**Output Format:** [JSON, CSV, XML, YAML, HTML, Markdown, query-string data, or date/time text returned from remote tool calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Inputs are submitted as string parameters to AgentPMT-hosted conversion actions; malformed input may return validation errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
