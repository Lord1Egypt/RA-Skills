## Description: <br>
Anticipates needs, keeps work moving, and improves through use so the agent gets more proactive over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjtmatch](https://clawhub.ai/user/wjtmatch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help an agent maintain local proactive operating state, recover active task context, suggest useful next steps, and follow through within explicit boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local proactive notes under ~/proactivity/ may accumulate sensitive personal or project details over time. <br>
Mitigation: Review or clear those files periodically and avoid storing secrets or sensitive personal details there. <br>
Risk: Proactive workspace integration could change files outside the local proactivity state if approved without review. <br>
Mitigation: Approve workspace-file changes only after reading the exact proposed snippet or diff. <br>
Risk: Heartbeat follow-ups and reverse prompts can become noisy if they are not tied to clear value. <br>
Mitigation: Use heartbeat messaging only when something changed, a decision is needed, or a prepared draft or recommendation is ready. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wjtmatch/tmp-proactivity-review) <br>
- [Publisher Profile](https://clawhub.ai/user/wjtmatch) <br>
- [Skill Homepage](https://clawic.com/skills/proactivity) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local proactivity notes and proposed configuration snippets; workspace edits outside ~/proactivity/ require explicit approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
