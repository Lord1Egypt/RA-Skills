## Description: <br>
Render an STL file to a PNG image with a deterministic software renderer and adjustable 3D perspective parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajmwagar](https://clawhub.ai/user/ajmwagar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create consistent preview or marketing PNG images from ASCII or binary STL models without depending on Blender or OpenGL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper downloads Pillow from PyPI into a cached Python virtual environment on first use. <br>
Mitigation: For stricter environments, preinstall or pin dependencies before use. <br>
Risk: The renderer reads an STL input path and writes a PNG output path supplied at runtime. <br>
Mitigation: Pass only the input and output paths the agent is intended to access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ajmwagar/render-stl-png) <br>
- [Publisher profile](https://clawhub.ai/user/ajmwagar) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [PNG image files with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts STL input and PNG output paths plus optional image size, colors, camera angles, field of view, margin, and light direction.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
