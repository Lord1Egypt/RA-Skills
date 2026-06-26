## Description: <br>
Trace bitmap images (PNG/JPG/WebP) into clean SVG paths using potrace/mkbitmap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajmwagar](https://clawhub.ai/user/ajmwagar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to convert high-contrast bitmap logos, silhouettes, and reference images into SVG paths for CAD or manufacturing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script creates parent directories and writes the SVG to the specified output path. <br>
Mitigation: Check the input image and output path before running the command. <br>
Risk: The skill depends on local potrace and mkbitmap binaries. <br>
Mitigation: Install dependencies only from trusted package managers. <br>
Risk: Photos or complex shaded images may trace poorly because output depends on thresholding and cleanup settings. <br>
Mitigation: Use high-contrast images when possible and tune threshold, turdsize, alphamax, and opttolerance for noisy inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ajmwagar/trace-to-svg) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration, files] <br>
**Output Format:** [Markdown with inline bash commands and SVG file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The tracing script writes an SVG file to the requested output path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
