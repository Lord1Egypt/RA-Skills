## Description: <br>
Tool safety and reliability guidance for agents that need to handle repeated tool failures, permission-denial retry loops, destructive-operation safeguards, and Bash input validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add tool-governance patterns for retry escalation, denial tracking, destructive-command checkpointing, permission rules, scoped hooks, and Bash input guards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recommend powerful hook behavior that blocks or rewrites commands and changes git state through checkpointing. <br>
Mitigation: Review hook configuration before installation and enable these hooks only in repositories where automatic blocking, command rewriting, and git stash checkpoints are acceptable. <br>
Risk: Shared-context state files may contain tool inputs, error details, denial records, or other sensitive workflow information. <br>
Mitigation: Treat generated state files as sensitive, restrict access to session storage, and avoid publishing logs or state files without review. <br>
Risk: Tracking and rollback controls may not run if hooks are registered on the wrong events or deployed without their companion scripts. <br>
Mitigation: Verify that tracker and advisor hooks are installed together and test the intended PreToolUse, PostToolUseFailure, and Stop event paths before relying on the safeguards. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/tool-governance) <br>
- [Tool Error Retry Escalation](references/tool-error.md) <br>
- [Denial Circuit Breaker](references/denial-circuit-breaker.md) <br>
- [Checkpoint Rollback](references/checkpoint-rollback.md) <br>
- [Graduated Permissions](references/graduated-permissions.md) <br>
- [Component-Scoped Hooks](references/scoped-hooks.md) <br>
- [Tool Input Guard](references/tool-input-guard.md) <br>
- [Extended Tool Governance Patterns](references/extended-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell hook scripts and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or recommend hook state files such as tool error records, denial records, and git stash checkpoints.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
