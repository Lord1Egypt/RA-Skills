## Description: <br>
Generate SVGs from text prompts and convert raster images (PNG/JPG/WebP) to SVG using QuiverAI's AI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lolieatapple](https://clawhub.ai/user/lolieatapple) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and other external users use this skill to generate SVG icons, illustrations, and logos from prompts or to vectorize PNG, JPG, and WebP images with the QuiverAI CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, private URLs, proprietary designs, or sensitive images may be sent to the external QuiverAI service. <br>
Mitigation: Use the skill only with content approved for processing by QuiverAI, and avoid confidential prompts, sensitive images, and private design assets unless that external use is acceptable. <br>
Risk: Generated SVG output paths can overwrite existing files if filenames are chosen carelessly. <br>
Mitigation: Choose deliberate output filenames and inspect the generated file path before running the CLI command. <br>
Risk: The skill depends on a separately installed QuiverAI CLI and API key configuration. <br>
Mitigation: Install the CLI from a trusted source, configure the API key intentionally, and run the skill only in workspaces where that dependency is expected. <br>


## Reference(s): <br>
- [QuiverAI Skill on ClawHub](https://clawhub.ai/lolieatapple/quiver-ai-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated SVG file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the quiver CLI to save generated or vectorized SVG files to explicit output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
