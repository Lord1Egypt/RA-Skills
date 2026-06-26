## Description: <br>
Deep cleans Windows C drive junk files by scanning disk usage and guiding cleanup of caches, temp files, logs, browser data, application caches, Windows Store, .NET, game, and video-conferencing caches while protecting user data and system stability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ftois](https://clawhub.ai/user/ftois) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and support engineers use this skill to scan Windows C drive storage pressure, identify cleanup candidates, and execute or review cleanup commands for temporary files, caches, logs, browser data, app caches, and other low-value disk usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aggressive automatic deletion can remove data or application state that the user expected to keep. <br>
Mitigation: Run scan-only first and require explicit approval before any deletion. <br>
Risk: VSS resizing, DISM resetbase, and Recycle Bin emptying can reduce recovery options or permanently remove recoverable files. <br>
Mitigation: Treat each recovery-impacting action as a separate opt-in step with a clear explanation before execution. <br>
Risk: Browser data removal, Desktop cleanup, user-profile recursive matches, and old app-version deletion may affect user workflows or application state. <br>
Mitigation: Review matched paths and categories with the user before cleanup, and skip uncertain or user-owned content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ftois/win-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell command blocks and cleanup summary tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scan-first cleanup workflow; deletion and recovery-impacting actions require user supervision.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
