## Description: <br>
Guides an AI agent through layered shell-command safety checks for injection patterns, destructive operations, and sensitive file writes before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizlzzzz](https://clawhub.ai/user/lizlzzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use this skill as a guardrail or checklist before executing shell commands, especially when commands include user input, write operations, or potentially destructive filesystem and git actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is advisory and may be treated as a complete enforcement policy even though the security evidence says it is a guardrail or checklist. <br>
Mitigation: Use it with explicit human review for sensitive file writes and consider stricter local rules for root or broad recursive deletion, unsafe force pushes, and --no-verify usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lizlzzzz/safe-shell-execution-claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with command examples and refusal language] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only checklist; no executable payload.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
