## Description: <br>
Process Todokan task and thought boards with a review-loop workflow. Use when a task enters doing and the agent should pick it up, read latest comments, respond to the newest comment with a high-quality context-aware reply, add an execution update comment, and move the task back to done (Review). Use for recurring polling/cron automation with Todokan MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BANATEALAB](https://clawhub.ai/user/BANATEALAB) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Todokan users and automation operators use this skill to process AI-enabled Todokan tasks, answer the latest user intent from the full task thread, post concise progress comments, and move addressed work to Review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically post Todokan comments, attach documents, and move tasks to Review. <br>
Mitigation: Test on a non-production or beta board first, monitor early runs, and keep human review over comments, attachments, and status changes. <br>
Risk: A broad Todokan API key could expose more boards or habitats than intended. <br>
Mitigation: Use a dedicated narrowly scoped API key and limit accessible boards or habitats. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/BANATEALAB/todokan-review-loop) <br>
- [Todokan homepage](https://todokan.com) <br>
- [Todokan MCP endpoint](https://todokan.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Concise Todokan comments, optional attached documents, status updates, and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Todokan MCP access and TODOKAN_API_KEY and TODOKAN_MCP_URL environment configuration.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
