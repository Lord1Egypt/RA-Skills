## Description:

Control Rhino 3D via the RhinoClaw plugin over TCP to create, modify, query, measure, or render 3D geometry, manage layers and materials, run Boolean and transform operations, drive Grasshopper definitions, work with VisualARQ BIM objects, or batch multiple steps as one atomic operation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcmuff86](https://clawhub.ai/user/mcmuff86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and automation agents use RhinoClaw to automate live Rhino 3D sessions for modeling, scene inspection, rendering, Grasshopper execution, and VisualARQ BIM workflows. It is intended for environments where Rhino 7 or 8 and the RhinoClaw plugin server are already running.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mutate a live Rhino model and may clear, delete, save, export, run Boolean or solid edits, execute native commands, or run arbitrary scripts.

Mitigation: Require explicit human confirmation for destructive or high-impact operations and keep backups or saved copies of important models before agent-driven changes.

Risk: The skill communicates with a Rhino plugin server over TCP and can be misconfigured or exposed without adequate authentication.

Mitigation: Use a RhinoClaw auth token, run preflight before other operations, and only proceed when the connection and authentication state is ready.

Risk: Raw scripting and native commands can bypass the safer typed helper layer.

Mitigation: Prefer typed helpers and batch operations, reserving RhinoScript, RhinoCommon, or native-command execution for cases where no typed helper covers the task.

## Reference(s):

- [RhinoClaw Command Reference](artifact/references/commands.md)
- [RhinoClaw project repository](https://github.com/McMuff86/rhinoclaw)
- [RhinoClaw release repository](https://github.com/McMuff86/rhinoclaw-release)
- [RhinoCommon API](https://developer.rhino3d.com/api/rhinocommon/)
- [Rhino.Python guide](https://developer.rhino3d.com/guides/rhinopython/)
- [RhinoScriptSyntax API](https://developer.rhino3d.com/api/RhinoScriptSyntax/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API Calls]

**Output Format:** [Markdown with inline shell commands, Python snippets, and JSON command payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue live Rhino TCP commands through typed helpers, batch operations, Grasshopper workflows, native commands, or Rhino Python execution.]

## Skill Version(s):

0.7.5 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
