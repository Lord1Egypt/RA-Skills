## Description:

AI-driven Unity3D game development assistant that helps developers manage scenes, generate C# scripts, optimize assets, automate builds, and support debugging and testing through a local Unity Editor bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cx75227-ops](https://clawhub.ai/user/cx75227-ops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to automate Unity Editor workflows, generate reusable C# gameplay templates, inspect scenes, manage assets, and run local build or play-mode actions from an agent-assisted workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes an unauthenticated local Unity control bridge that can modify projects, write code, delete objects, open scenes, enter Play Mode, and start builds.

Mitigation: Use it only on version-controlled Unity projects; keep the bridge stopped when not actively using it; avoid untrusted local processes or webpages while it is running; add authentication, path validation, and confirmations before using mutating endpoints.

Risk: Generated scripts, templates, and build actions can introduce broken gameplay code or unintended Unity project changes.

Mitigation: Review generated C# and build settings before applying them, test in a disposable branch or project copy, and run Unity validation or build checks before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cx75227-ops/skills/unity3d-game-dev)
- [Publisher profile](https://clawhub.ai/user/cx75227-ops)
- [SKILL.md](artifact/SKILL.md)
- [TEMPLATES.md](artifact/TEMPLATES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline commands, generated C# code, PowerShell commands, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May interact with a local Unity Editor bridge when the user installs and starts the bridge server.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
