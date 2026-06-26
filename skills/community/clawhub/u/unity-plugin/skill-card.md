## Description: <br>
Control Unity Editor via OpenClaw Unity Plugin for Unity game development tasks including scene management, GameObject and component manipulation, debugging, input simulation, and Play mode control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mlichao456](https://clawhub.ai/user/mlichao456) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect an agent workflow to Unity Editor for inspecting scenes, changing GameObjects, running editor actions, managing assets and packages, testing gameplay, and collecting debug output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Unity Editor control can modify scenes, assets, packages, scripts, saved project state, and runtime input. <br>
Mitigation: Use only on backed-up or version-controlled Unity projects and require explicit human review before script.execute, package.add from Git, deletion, save, batch execution, or input simulation. <br>
Risk: Exposing the Unity gateway or bridge beyond trusted local access could allow unintended editor control. <br>
Mitigation: Keep the gateway local or otherwise network-restricted, and install the extension only when Unity Editor control is intentionally required. <br>
Risk: Changing automated invocation settings can reduce oversight of project-changing tool calls. <br>
Mitigation: Keep automated tool invocation disabled unless the operator deliberately accepts autonomous Unity tool use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mlichao456/unity-plugin) <br>
- [Skill Homepage](https://github.com/TomLeeLive/openclaw-unity-skill) <br>
- [Unity Tool Reference](references/tools.md) <br>
- [OpenClaw Unity Plugin](https://github.com/TomLeeLive/openclaw-unity-plugin) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and Unity tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Unity tool names and JSON-like parameters for unity_execute.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.6.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
