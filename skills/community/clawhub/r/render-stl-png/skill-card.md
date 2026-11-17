## Description:

Render an ASCII or binary STL file to a PNG preview image with deterministic software rasterization and adjustable camera, color, lighting, and size parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajmwagar](https://clawhub.ai/user/ajmwagar)

### License/Terms of Use:


## Use Case:

Developers and technical content creators use this skill to generate consistent PNG preview images from STL models without requiring Blender or OpenGL. It is suited for quick product, documentation, or marketing previews where deterministic rendering is more important than photorealism.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper creates a cached Python virtual environment and downloads Pillow before rendering.

Mitigation: Review the wrapper behavior, preinstall dependencies in a controlled environment, or run the renderer with an approved Python environment.

Risk: Untrusted or very large STL files, or extreme --size values, can create availability or resource-consumption risk.

Mitigation: Render trusted files where possible and use CPU, memory, time, and output-size limits for untrusted or large inputs.

## Reference(s):

- [Render Stl Png on ClawHub](https://clawhub.ai/ajmwagar/skills/render-stl-png)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image file plus Markdown or shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces square PNG previews from STL input; supports size, background color, mesh color, camera azimuth/elevation, field of view, margin, and directional light settings.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
