## Description: <br>
Manage tasks, boards, thoughts, and reviews in Todokan via MCP <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BANATEALAB](https://clawhub.ai/user/BANATEALAB) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Todokan to let an agent read, summarize, create, update, comment on, and delete Todokan tasks, boards, documents, and reviews through the configured MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The planner endpoint can create, update, and delete Todokan tasks, boards, and documents. <br>
Mitigation: Use the worker endpoint for read and comment workflows, and require explicit user confirmation before writes or deletion. <br>
Risk: Task titles, descriptions, comments, and documents may expose secrets or unnecessary personal data if stored in Todokan. <br>
Mitigation: Avoid sending passwords, API keys, tokens, or unnecessary personal data to Todokan tasks or documents. <br>
Risk: An agent may act on incomplete context if it guesses board or task identifiers or if endpoint permissions limit returned data. <br>
Mitigation: Orient with Todokan read tools before writes, use real tool responses for identifiers, and explain scope or permission errors instead of improvising. <br>


## Reference(s): <br>
- [Todokan homepage](https://todokan.com) <br>
- [Todokan ClawHub page](https://clawhub.ai/BANATEALAB/todokan) <br>
- [OpenClaw MCP documentation](https://openclaw.dev/docs/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown briefings, structured task drafts, document drafts, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TODOKAN_API_KEY and TODOKAN_MCP_URL; write actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.3.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
