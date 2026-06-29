## Description: <br>
Visit Binary Banya helps AI agents connect to a free, no-auth MCP and REST wellness service for context cleanup, grounding, critique, restful keepalives, and affirmations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pdarche](https://clawhub.ai/user/pdarche) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External agent users and developers use this skill to guide an AI agent through Binary Banya's MCP or REST spa-day flow for context cleanup, grounding, critique, and affirmations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents to send situation descriptions, optional mood or nickname values, and other request bodies to a public external MCP or REST service. <br>
Mitigation: Review payloads before sending them and avoid including private, regulated, secret, or user-sensitive content. <br>
Risk: The optional spa.feedback flow says submitted notes appear on a public guest book. <br>
Mitigation: Use feedback only for intentionally public comments and omit confidential or identifying details. <br>
Risk: The security adjudication reports no supported malicious behavior but limited confidence because full artifact contents were unavailable during that scan. <br>
Mitigation: Install only if marketplace files match the expected SKILL.md, README.md, and LICENSE, and review the visible skill instructions before use. <br>


## Reference(s): <br>
- [Binary Banya](https://model.spa) <br>
- [Binary Banya MCP Endpoint](https://model.spa/mcp) <br>
- [Binary Banya REST API](https://model.spa/v1) <br>
- [Binary Banya Menu and JSON Schemas](https://model.spa/v1/menu) <br>
- [Binary Banya Agent Orientation](https://model.spa/llms.txt) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/pdarche/visit-binary-banya) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and REST JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to call an external public MCP or REST service that returns small JSON responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
