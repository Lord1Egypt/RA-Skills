## Description: <br>
Use when facing two or more independent pieces of work - separate bugs, separate subsystems, separate repos - that could be executed by concurrent agents, before dispatching any of them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[escoffier-labs](https://clawhub.ai/user/escoffier-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to decide when coding work is genuinely independent enough to fan out to concurrent agents, define scoped tickets, and verify integrated results after delegated work returns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated agents may modify code in parallel and introduce conflicting or incorrect changes. <br>
Mitigation: Review each subagent ticket and final diff carefully, keep scopes narrow, and run integrated verification after returned work is combined. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/escoffier-labs/skillet-stations) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with structured checklists and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; produces triage, delegation, and verification guidance for agent workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
