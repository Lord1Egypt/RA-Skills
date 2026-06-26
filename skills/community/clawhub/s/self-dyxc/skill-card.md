## Description: <br>
Self-reflection, self-criticism, self-learning, and self-organizing memory for agents that evaluate their work, record corrections, and improve over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mifashion](https://clawhub.ai/user/mifashion) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent maintain local memory about corrections, preferences, and reusable work patterns. It is intended for improving agent behavior across sessions while keeping stored memory auditable and scoped. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores durable local memory about user corrections, preferences, and work patterns. <br>
Mitigation: Review the contents of ~/self-improving/ regularly and avoid storing credentials, sensitive personal data, medical data, financial data, or third-party information. <br>
Risk: Workspace steering files such as AGENTS.md, SOUL.md, or HEARTBEAT.md may change agent behavior after setup. <br>
Mitigation: Review any workspace steering changes before relying on them and keep the memory mode scoped to the desired project or domain. <br>
Risk: Forgetting or export requests may not match user expectations if the affected memory files are not checked. <br>
Mitigation: Verify exports and deletion results by inspecting the updated memory files after the operation completes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mifashion/self-dyxc) <br>
- [Publisher profile](https://clawhub.ai/user/mifashion) <br>
- [Skill homepage](https://www.sztv.com.cn/ysz/zx/zw/80706997.shtml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files under ~/self-improving/ and optional workspace steering files when activated by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
