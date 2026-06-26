## Description: <br>
Human-in-the-loop MCP feedback collector with task queue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2019-02-18](https://clawhub.ai/user/2019-02-18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent users use this skill to pause an agent workflow for human confirmation, collect browser-based feedback, and optionally dispatch queued follow-up tasks before the agent continues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The feedback UI and WebSocket server can expose saved feedback and send instructions to the agent if reachable without authentication. <br>
Mitigation: Set FEEDBACK_TOKEN, restrict access with a firewall, and do not expose port 18061 publicly. <br>
Risk: Queued tasks are returned to the agent as instructions to execute. <br>
Mitigation: Review queued tasks before enabling auto-dequeue or using the tool on shared networks. <br>
Risk: Feedback history is persisted locally and may contain sensitive information. <br>
Mitigation: Review, rotate, or delete feedback-history.json regularly and avoid sending secrets through feedback. <br>
Risk: The evidence guidance notes that the browser flow may not forward FEEDBACK_TOKEN to API or WebSocket calls. <br>
Mitigation: Test the browser flow carefully when relying on FEEDBACK_TOKEN before using the skill in a shared environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2019-02-18/skill-feedback-collector) <br>
- [Publisher profile](https://clawhub.ai/user/2019-02-18) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration] <br>
**Output Format:** [MCP tool text responses with Markdown setup guidance and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns human feedback text, feedback-mode status text, or the next queued task as a single response stream.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
