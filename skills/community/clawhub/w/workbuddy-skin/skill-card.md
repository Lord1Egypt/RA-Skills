## Description:

Helps build, modify, debug, and publish a Windows WorkBuddy Skin Studio desktop skinning tool using Tauri v2 and Rust.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pddsa](https://clawhub.ai/user/pddsa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or update a Windows WorkBuddy GUI skinning workflow, including theme application, local CDP-based styling, WorkBuddy path handling, custom skin behavior, and NSIS packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow involves running npm, Tauri, and Rust desktop build commands.

Mitigation: Inspect the copied template, require a committed lockfile, prefer npm ci, pin the Tauri CLI, and build in a clean environment without unrelated credentials.

Risk: Theme application relies on a local CDP connection to WorkBuddy.

Mitigation: Keep CDP bound to 127.0.0.1 and do not expose the connection on a LAN or public interface.

Risk: Packaging or skin changes could alter WorkBuddy installation files if applied outside the documented boundary.

Mitigation: Do not modify WorkBuddy app.asar, installation directories, or signature files; distribute only the NSIS setup artifact described by the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pddsa/skills/workbuddy-skin)
- [Server-resolved GitHub source](https://github.com/PDDsa/WorkBuddy-skin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code/configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
