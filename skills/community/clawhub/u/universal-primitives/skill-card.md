## Description: <br>
Universal Primitives explains a minimal agent architecture in which file operations and command execution enable an LLM to create, modify, run, and iterate on software-mediated tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and technical reviewers use this skill to reason about agent capability boundaries, minimal tool design, and how file access plus command execution can expand an LLM's operational reach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill discusses creating or expanding execution channels through file operations, command execution, online sandboxes, software control, and hardware interfaces. <br>
Mitigation: Use it only in environments with explicit user approval, bounded file and command permissions, and review of the exact task, files, environment, and limits before any action. <br>
Risk: The skill does not define clear safety limits for agents that gain file access or command execution. <br>
Mitigation: Apply external policy controls, sandboxing, command allowlists, and human review before permitting file changes, software installation, networked execution, or hardware operation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangjiaocheng/universal-primitives) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with conceptual examples and command-oriented instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; it does not bundle executable code.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
