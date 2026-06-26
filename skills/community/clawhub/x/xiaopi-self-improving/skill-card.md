## Description: <br>
An agent memory skill that records command errors, user corrections, and best practices so future sessions can check and reuse those local memories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a-din](https://clawhub.ai/user/a-din) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to persist local memories about failed commands, user corrections, and preferred practices, then check those memories before repeating similar work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to persist conversation-derived memories that can influence future agent behavior. <br>
Mitigation: Require explicit approval before writing to AGENTS.md, MEMORY.md, .learnings, or git-tracked files, and periodically review stored memories. <br>
Risk: Memory entries may accidentally capture sensitive information or unsafe system-changing guidance. <br>
Mitigation: Avoid storing secrets, redact sensitive values, and require fresh confirmation before applying remembered fixes involving sudo, global installs, or other system-changing commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a-din/xiaopi-self-improving) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/a-din) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local JSONL memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads local memory records under ~/.openclaw/memory/self-improving when its scripts are invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
