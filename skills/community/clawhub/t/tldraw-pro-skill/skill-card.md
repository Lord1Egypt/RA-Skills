## Description:

Generates tldraw whiteboard diagrams as .tldr JSON files and exports them to PNG or SVG using @kitschpatrol/tldraw-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and agent users use this skill to turn architecture, flowchart, sequence, ML, ERD, and UML requests into editable whiteboard-style diagrams with exported image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently self-update and can install a global npm tool without explicit user approval.

Mitigation: Disable or remove the auto-update step, require explicit approval for git pulls, and install @kitschpatrol/tldraw-cli manually or as a pinned local dependency.

Risk: Diagram outputs may be written outside the intended workspace when a user-supplied path is accepted.

Mitigation: Keep exports in a known workspace directory and review output paths before running file creation or export commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agents365-ai/skills/tldraw-pro-skill)
- [tldraw](https://tldraw.com)
- [Agent Skills format](https://agentskills.io)
- [Skill homepage](https://github.com/Agents365-ai/tldraw-skill)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [.tldr JSON files, PNG/SVG exports, and Markdown progress or file-path summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and the tldraw CLI; vision-based self-check is skipped when the active model lacks image input.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
