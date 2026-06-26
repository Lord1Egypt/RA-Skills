## Description: <br>
Comprehensive AI-assisted therapeutic support framework with CBT, ACT, DBT, motivational interviewing, session notes, and crisis protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSethRose](https://clawhub.ai/user/TheSethRose) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to provide structured AI-assisted mental-health support, including therapeutic conversation patterns, coping exercises, risk escalation guidance, and session note continuity. It is not a substitute for licensed professional care or emergency services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Therapy conversations and mental-health notes may be written to persistent local plaintext files. <br>
Mitigation: Use the skill only when users understand what is stored and where; prefer opt-in note taking, restrictive file permissions, secure storage, and clear retention or deletion practices. <br>
Risk: The bundled notes CLI uses a hardcoded local notes path that does not match the documented workspace location. <br>
Mitigation: Replace the hardcoded path with the actual workspace path before broad use and verify note commands operate only in the intended directory. <br>
Risk: The notes CLI includes permanent deletion of session files. <br>
Mitigation: Keep destructive actions explicit, confirmed, and reversible where possible; use archive or restore workflows when deletion is not required. <br>


## Reference(s): <br>
- [Therapy Mode ClawHub release](https://clawhub.ai/TheSethRose/therapy-mode) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and local plaintext session-note files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, read, update, archive, restore, or delete local therapy session notes when the included CLI is used.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
