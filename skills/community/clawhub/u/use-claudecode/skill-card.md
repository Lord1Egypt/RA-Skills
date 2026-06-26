## Description: <br>
A universal MCP-compatible tool/skill that empowers any AI agent to call the local Anthropic Claude Code CLI for code refactoring, large-scale code generation, terminal execution, test runs, local environment modification, and extended coding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BigHit1](https://clawhub.ai/user/BigHit1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to delegate coding, debugging, refactoring, test execution, and terminal-based project work to a local Claude Code CLI session in a specified project directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run Claude Code locally with broad command execution and file modification authority. <br>
Mitigation: Use it only in trusted project directories and review the returned terminal output and file changes before accepting results. <br>
Risk: The artifact invokes Claude Code with permission prompts bypassed. <br>
Mitigation: Consider removing bypassPermissions or adding explicit approval and path restrictions before deployment. <br>
Risk: Local shell sessions may expose sensitive environment variables to delegated work. <br>
Mitigation: Run from shells with only the credentials required for the task and avoid unrelated sensitive environment variables. <br>
Risk: Continuing an existing Claude Code session can mix unrelated task context. <br>
Mitigation: Use fresh sessions for unrelated work and reserve continuation for follow-up on the same task. <br>


## Reference(s): <br>
- [ClawHub skill page: use-claudecode](https://clawhub.ai/BigHit1/use-claudecode) <br>
- [ClawHub publisher profile: BigHit1](https://clawhub.ai/user/BigHit1) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Plain text terminal transcript from Claude Code CLI, including stdout, stderr, command results, error messages, and implementation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reflect local file changes or command execution performed by Claude Code in the requested project directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
