## Description: <br>
This skill should be used when the user asks to "create a multi-agent system", "spawn agents for parallel tasks", "decompose task recursively", "set up agent matrix", or wants to execute complex tasks using multiple coordinated agents with conflict-free parallel processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyijun](https://clawhub.ai/user/cyijun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Smith Matrix to organize complex work into recursive, bounded multi-agent task folders with directory-based inbox, outbox, private workspace, and child-agent conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task descriptions and private notes may expose sensitive information if generated .smith-matrix files are shared or committed. <br>
Mitigation: Avoid placing secrets in tasks or notes, and review generated .smith-matrix files before sharing, committing, or publishing them. <br>
Risk: Directory isolation is an agent protocol, not a hard security sandbox. <br>
Mitigation: Run the skill in a constrained workspace and review file changes before relying on generated outputs. <br>
Risk: Recursive task decomposition can create unnecessary local files or coordination overhead if used on simple tasks. <br>
Mitigation: Apply the documented recursion limits: maximum level 3, at most 5 child agents per level, and direct execution at terminal levels. <br>


## Reference(s): <br>
- [Smith Matrix on ClawHub](https://clawhub.ai/cyijun/smith-matrix) <br>
- [Core Concepts](references/concepts.md) <br>
- [Conflict-Free Protocol](references/protocol.md) <br>
- [Best Practices](references/best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and local workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces .smith-matrix task, private, outbox, children, and results files when applied by an agent.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
