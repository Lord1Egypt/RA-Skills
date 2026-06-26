## Description: <br>
Renders LaTeX math to PNG, JPEG, WebP, or AVIF images using MathJax for TeX-to-SVG conversion and @svg-fns/svg2img. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheBigoranger](https://clawhub.ai/user/TheBigoranger) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to render LaTeX equations as image files or Data URLs for chat, docs, or slides instead of returning raw LaTeX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendered files can be written to local paths, including custom output paths supplied at invocation time. <br>
Mitigation: Use the default output directory unless a trusted custom path is required, and do not pass untrusted output paths. <br>
Risk: Installing the skill requires npm dependencies, including a native image-processing dependency. <br>
Mitigation: Review the npm dependency chain before running npm install and install in an environment prepared for the documented Node.js and build-tool requirements. <br>
Risk: When enabled for automatic LaTeX handling, the skill may render and send formula images without a separate permission prompt. <br>
Mitigation: Enable it only when automatic LaTeX image rendering is desired, and document the behavior in workspace guidance for users who prefer raw LaTeX. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheBigoranger/tex-render) <br>
- [MathJax](https://github.com/mathjax/MathJax) <br>
- [@svg-fns/svg2img](https://github.com/svg-fns/svg-fns) <br>
- [Sharp install notes](https://sharp.pixelplumbing.com/install) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration, guidance] <br>
**Output Format:** [JSON paths to SVG and raster image files, with optional Data URL output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default file output writes under ~/.openclaw/media/tex-render/; custom output paths and Data URL mode are available.] <br>

## Skill Version(s): <br>
1.1.4 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
