## Description:

Write, explain, debug, and port ShaderToy-style fragment shaders for tasks involving mainImage, fragCoord, ShaderToy built-ins, channels, buffers, and migration to WebGL, Three.js, React Three Fiber, or browser canvas demos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write, explain, debug, and port ShaderToy-style fragment shaders while preserving ShaderToy-specific concepts such as mainImage, built-ins, channels, buffers, and feedback passes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated shader or browser demo code can be incorrect, visually misleading, or fail at runtime when copied into ShaderToy, WebGL, Three.js, React Three Fiber, or a browser canvas.

Mitigation: Review generated shader and demo code before running it, test with simple visible outputs first, and validate ShaderToy built-ins, channels, buffers, and uniforms one step at a time.

Risk: A multi-pass or feedback-based ShaderToy effect may be treated as a single-pass effect, producing blank, unstable, or incomplete output.

Mitigation: Identify Buffer A/B/C/D usage, previous-frame dependencies, pass ordering, and render-target or ping-pong buffer requirements before porting.

## Reference(s):

- [ShaderToy Built-ins](references/builtins.md)
- [ShaderToy Porting](references/porting.md)
- [Buffers and Feedback](references/buffers-feedback.md)
- [ShaderToy feedback export notes](assets/shadertoy-feedback-notes.txt)
- [ShaderToy single-pass demo](assets/shadertoy-single-pass-demo/index.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, code blocks, shell commands, JSON helper output, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include corrected ShaderToy fragment shaders, built-in-to-uniform mappings, porting plans, debug checklists, and scaffold recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
