## Description: <br>
Connect OpenClaw to a paid QwryAI workspace through the read-only QwryAI MCP and public API integration surface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tamjeedhur](https://clawhub.ai/user/tamjeedhur) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and customer support teams use this skill to let an agent inspect a paid QwryAI workspace, including chatbots, conversations, messages, knowledge search results, analytics, and account context. The skill is intended for read-only review and reporting, not for replying to customers or changing workspace resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive QwryAI API key and gives the chosen agent read-only access to selected workspace data. <br>
Mitigation: Store QWRYAI_API_KEY in an environment variable or secret manager, avoid committing resolved tokens, and install only when the agent and QwryAI workspace access are trusted. <br>
Risk: Endpoint overrides could route requests away from QwryAI's hosted production API. <br>
Mitigation: Keep QWRYAI_MCP_URL and QWRYAI_API_URL pointed at the official QwryAI HTTPS host unless you deliberately manage an alternative. <br>
Risk: The integration is designed for read-only access, while customer replies, workspace edits, billing changes, user management, and admin actions are outside its intended scope. <br>
Mitigation: Use the skill for inspection, search, analytics, and summaries only; do not ask the agent to perform write or administrative actions. <br>


## Reference(s): <br>
- [QwryAI ClawHub Release](https://clawhub.ai/tamjeedhur/qwryai) <br>
- [QwryAI Publisher Profile](https://clawhub.ai/user/tamjeedhur) <br>
- [QwryAI Homepage](https://qwryai.com) <br>
- [QwryAI MCP Endpoint](https://api.qwryai.com/mcp) <br>
- [QwryAI Public API Endpoint](https://api.qwryai.com/public/v1) <br>
- [QwryAI Claude OAuth MCP Endpoint](https://api.qwryai.com/mcp-oauth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only agent guidance for connecting to hosted QwryAI MCP and public API endpoints.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
