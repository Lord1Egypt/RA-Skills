## Description: <br>
Helps OpenClaw agents find prior conversations, review message history, and bring selected historical context into current or new sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linshuikeji](https://clawhub.ai/user/linshuikeji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect previous session records, recover work context, audit session activity, and selectively reuse relevant history in ongoing work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Historical conversations may contain secrets, personal data, or other sensitive context. <br>
Mitigation: Review history before reuse, remove secrets and personal data, and prefer summaries or selected excerpts. <br>
Risk: Forwarding large or irrelevant history into another session can disclose unnecessary context or confuse the agent. <br>
Mitigation: Keep retrieval limits small and send only the conversation segments needed for the current task. <br>
Risk: Exported session history files can persist sensitive content after the immediate task is complete. <br>
Mitigation: Delete exported files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linshuikeji/session-history-retriever-clean) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw Session Concepts](https://docs.openclaw.ai/concepts/session) <br>
- [OpenClaw Compaction Concepts](https://docs.openclaw.ai/concepts/compaction) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include session keys, limits, labels, and privacy handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
