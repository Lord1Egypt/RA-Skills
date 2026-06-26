## Description: <br>
Records command errors, user corrections, and best practices as local memory so an agent can check prior lessons before repeating work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a-din](https://clawhub.ai/user/a-din) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to persist local lessons from failed commands, user corrections, and better practices, then check those records before future command execution or workflow decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can influence future agent behavior after the original context is gone. <br>
Mitigation: Require explicit confirmation before saving memories and periodically review stored records for accuracy, sensitivity, and continued relevance. <br>
Risk: Automatic writes to AGENTS.md, MEMORY.md, .learnings, or git backups can change project instructions without clear approval. <br>
Mitigation: Disable automatic instruction-file and backup writes unless a human reviews and approves each proposed change. <br>
Risk: Stored memories could suggest privileged commands such as sudo retries without enough review. <br>
Mitigation: Never allow stored memories to trigger sudo or other privileged commands without explicit review at execution time. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a-din/self-improving-agent-cn-skip) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/a-din) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSONL memory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads local memory files under the user's OpenClaw memory directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, skill.json, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
