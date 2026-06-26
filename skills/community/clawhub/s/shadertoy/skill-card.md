## Description: <br>
Write, explain, debug, and port ShaderToy-style fragment shaders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to write, troubleshoot, explain, and port ShaderToy fragment shaders that rely on mainImage, ShaderToy built-ins, channels, buffers, or feedback passes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate automatically for ShaderToy-like prompts. <br>
Mitigation: Review automatic invocations when prompts mention ShaderToy concepts but the task may require a broader shader or rendering workflow. <br>
Risk: The bundled Node helper prints shell-driven guidance and should be reviewed before use in sensitive environments. <br>
Mitigation: Inspect scripts/shadertoy.js before running helper commands and treat generated commands or checklists as proposals. <br>
Risk: Feedback or buffer-dependent ShaderToy effects can be misrepresented as single-pass shaders. <br>
Mitigation: Identify Image and Buffer A/B/C/D pass dependencies before porting and plan render targets or ping-pong buffers where needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jvy/shadertoy) <br>
- [ShaderToy built-ins](references/builtins.md) <br>
- [ShaderToy porting](references/porting.md) <br>
- [Buffers and feedback](references/buffers-feedback.md) <br>
- [ShaderToy feedback export notes](assets/shadertoy-feedback-notes.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, code blocks, JSON command output, and concise implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Node helper commands for built-in maps, channel triage, porting checklists, debug checklists, and scaffold recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
