## Description: <br>
Captures and logs choices, options, or prompts that the agent evaluated and decided NOT to execute. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balkanblbn](https://clawhub.ai/user/balkanblbn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to record rejected requests, skipped approaches, and selected alternatives in a persistent workspace audit log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent rejection logs can expose private context, prompts, secrets, or sensitive reasoning if recorded verbatim. <br>
Mitigation: Log only short sanitized summaries with user consent, avoid secrets and full prompts, and review .learnings/REJECTIONS.md before committing or sharing a workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/balkanblbn/rejection-logger) <br>
- [Publisher profile](https://clawhub.ai/user/balkanblbn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown rejection log entries and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends entries to .learnings/REJECTIONS.md when the bundled script is used.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
