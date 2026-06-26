## Description: <br>
Compress OpenClaw session .jsonl files to reduce context size while preserving active tasks, plans, and important context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzqsama066](https://clawhub.ai/user/zzqsama066) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to shrink large OpenClaw main-agent session files while retaining recent turns, system messages, and task-relevant context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compressing a session in place can permanently remove older session history. <br>
Mitigation: Run the documented dry run first and prefer an OutputPath or backup before overwriting the original file. <br>
Risk: The workflow references a compress.ps1 helper that is not included in this package. <br>
Mitigation: Confirm the helper exists in the intended environment and inspect it before running the commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown with PowerShell command examples and .jsonl session-file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode, configurable recent-turn retention, and optional output path for preserving the original session file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
