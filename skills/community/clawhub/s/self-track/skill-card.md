## Description: <br>
Self-Track helps an agent track autonomous growth by logging learning, capability gaps, self-review prompts, memory updates, and skill-building tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[louch84](https://clawhub.ai/user/louch84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain a structured self-improvement loop for tracking learning, capability gaps, weekly reviews, and memory updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage persistent long-term memory writes, including vector-memory updates. <br>
Mitigation: Require explicit user confirmation before writing to memory files or adding vector-memory entries. <br>
Risk: The skill includes broad self-improvement triggers that may activate outside a narrow task scope. <br>
Mitigation: Use it only when long-term self-improvement tracking is intended, and confirm the scope before logging or updating state. <br>
Risk: The skill includes skill creation, commit, and push instructions. <br>
Mitigation: Require explicit confirmation before creating new skills, committing changes, or pushing to a remote repository. <br>
Risk: The skill references local scripts for memory and skill workflows. <br>
Mitigation: Inspect referenced local scripts before allowing them to run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/louch84/self-track) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent memory updates, skill creation steps, and commit or push actions that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
