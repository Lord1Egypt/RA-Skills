## Description: <br>
Clean up stale or unwanted subagent sessions from the OpenClaw webchat sidebar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saybanet](https://clawhub.ai/user/saybanet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to preview and remove stale or unwanted subagent entries from local OpenClaw session indexes so the webchat sidebar reflects current sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Editing OpenClaw session sidebar indexes can remove session history the user intended to keep. <br>
Mitigation: Run with --dry-run first and back up sessions.json before applying cleanup. <br>
Risk: The --all option removes every matching subagent session entry, not only stale entries. <br>
Mitigation: Use --all only when intentionally clearing all matching subagent entries, and use --agent to narrow the target when appropriate. <br>


## Reference(s): <br>
- [Sayba Session Cleanup on ClawHub](https://clawhub.ai/saybanet/sayba-session-cleanup) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run, all-session cleanup, and target-agent command variants.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
