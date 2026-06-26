## Description: <br>
Helps an OpenClaw agent recall prior session history, find keyword context, and save selected conversation details into dated memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noir-hedgehog](https://clawhub.ai/user/noir-hedgehog) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to retrieve past conversation context, search for relevant session details, and preserve important decisions, tasks, and user-specific notes in memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can search broad prior conversation history and expose sensitive or personal details. <br>
Mitigation: Use it only for explicitly selected sessions or keywords and avoid reset or deleted logs unless deliberately needed. <br>
Risk: The skill can save personal details from conversations into memory files without clear retention limits. <br>
Mitigation: Review any memory content the skill writes before keeping it, and remove unnecessary personal information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noir-hedgehog/session-recall) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline command examples and memory-file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include extracted session summaries, keyword context, todo items, and dated memory entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
