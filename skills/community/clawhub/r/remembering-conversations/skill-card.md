## Description: <br>
Helps an agent decide when to search past conversation history and request summarized findings from a dedicated conversation-search agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YumoeZhung](https://clawhub.ai/user/YumoeZhung) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to decide when prior Claude Code conversations may help with architectural choices, stuck debugging, unfamiliar workflows, or explicit references to past work. It guides the agent to request a focused summary instead of loading raw conversation history directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Past conversation retrieval can expose secrets, credentials, personal data, tool outputs, or private project details. <br>
Mitigation: Use the narrowest search and read scope that answers the current question, and avoid retrieving unrelated conversation content. <br>
Risk: Direct memory-tool access can load more raw conversation content than needed. <br>
Mitigation: Route historical searches through the dedicated conversation-search agent and rely on concise synthesized findings with sources. <br>
Risk: Older conversation findings may be stale or not apply to the current codebase. <br>
Mitigation: Inspect current files and requirements first, then use memory as supporting context for decisions or troubleshooting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YumoeZhung/remembering-conversations) <br>
- [Episodic Memory MCP Tools Reference](MCP-TOOLS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Tool invocation instructions] <br>
**Output Format:** [Markdown with task prompts and tool invocation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results should be summarized into actionable findings with sources rather than loading full raw conversations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
