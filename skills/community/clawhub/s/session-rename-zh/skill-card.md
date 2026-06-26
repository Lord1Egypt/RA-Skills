## Description: <br>
Helps an OpenClaw agent rename sessions by adding a label to the local sessions.json metadata file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fhekg](https://clawhub.ai/user/fhekg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to set readable display names for current or selected OpenClaw sessions when the built-in CLI or RPC interface does not expose a rename command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill modifies OpenClaw's persistent local session metadata directly. <br>
Mitigation: Confirm the target session and requested label before writing, and back up sessions.json when the local state is important. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fhekg/session-rename-zh) <br>
- [Project homepage](https://github.com/fhekg/openclaw-session-rename) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for reading, updating, and verifying OpenClaw session metadata.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
