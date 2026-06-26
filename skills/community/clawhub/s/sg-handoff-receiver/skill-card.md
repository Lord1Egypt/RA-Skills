## Description: <br>
Receive a prior session handoff and continue execution safely by validating repo state, resuming from next steps, and refreshing the handoff artifact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to resume work from an existing handoff, validate repository state before making changes, and keep the active handoff, CURRENT pointer, and INDEX.md status current. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Handoff files may be stale, conflicting, or untrusted and could steer the agent toward the wrong work. <br>
Mitigation: Review CURRENT and INDEX.md first, compare the handoff to repository state, and ask a focused clarification question when the active stream or index is inconsistent. <br>
Risk: The skill intentionally updates local handoff state, including CURRENT, INDEX.md, and status fields. <br>
Mitigation: Review handoff file changes before committing or sharing them, especially in shared or untrusted repositories. <br>


## Reference(s): <br>
- [Handoff Receiver on ClawHub](https://clawhub.ai/clarezoe/sg-handoff-receiver) <br>
- [Resolved orphan handoffs note](RESOLVED/ISSUE-orphan-handoffs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown status text with inline bash code blocks and local handoff file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates are scoped to handoff state such as CURRENT, INDEX.md, and handoff status fields when the agent follows the skill.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata; artifact metadata reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
