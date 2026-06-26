## Description: <br>
Helps developers write, adapt, port, and debug practical browser-friendly shaders for GLSL, WebGL, Three.js ShaderMaterial, React Three Fiber, postprocess passes, and ShaderToy-style fragment effects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn visual effect requests into runnable shader code, host integration steps, and targeted debugging guidance. It is useful for creating effects, porting ShaderToy-style fragments to browser runtimes, wiring uniforms, and troubleshooting blank output or shader compile issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Demo templates and generated setup steps may include npm dependencies or local development servers. <br>
Mitigation: Review dependencies before use, avoid elevated privileges, and keep Vite development servers local unless network access is intentional. <br>
Risk: Generated shader code may fail visually because uniforms, varyings, precision, color space, or runtime assumptions do not match the host application. <br>
Mitigation: Start from the smallest visible shader, verify draw path and uniform data, and add effects incrementally using the bundled debugging checklist. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jvy/shader) <br>
- [GLSL Quick Reference](references/glsl-quick-reference.md) <br>
- [Black Screen Checklist](references/black-screen-checklist.md) <br>
- [Runtime Translation](references/runtime-translation.md) <br>
- [Shader Snippets](references/snippets.md) <br>
- [Shader Effect Starters](references/effect-starters-zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with GLSL, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference bundled snippets, local demo templates, and runtime-specific integration steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
