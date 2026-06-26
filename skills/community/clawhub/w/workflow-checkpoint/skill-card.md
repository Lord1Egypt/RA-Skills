## Description: <br>
Workflow Checkpoint helps agents save and recover progress during multi-step AI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aptratcn](https://clawhub.ai/user/aptratcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan long-running workflows, write checkpoint files after each step, and resume failed or interrupted work from the last verified checkpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkpoint files may capture sensitive data, tokens, user data, internal host details, or raw command output. <br>
Mitigation: Keep checkpoint contents minimal, avoid secrets and unnecessary raw outputs, and delete old checkpoint files when they are no longer needed. <br>
Risk: Resuming from stale or incomplete checkpoint state can cause the agent to skip needed work. <br>
Mitigation: Verify saved artifacts and step status before skipping completed steps during recovery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aptratcn/workflow-checkpoint) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON checkpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local checkpoint JSON files under memory/checkpoints when the agent follows the protocol.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
