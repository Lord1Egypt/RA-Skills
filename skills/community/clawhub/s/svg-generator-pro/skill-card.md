## Description: <br>
Generate customizable SVG backgrounds and graphics in tech, minimal, geometric, and abstract styles with selectable color schemes for websites, presentations, social media, and UI decorative elements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NimaChu](https://clawhub.ai/user/NimaChu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content creators use this skill to generate local SVG backgrounds and decorative graphics for websites, presentations, social posts, and interface mockups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SVG-to-PNG helper is described by security evidence as misleading and uses a simplified rendering path. <br>
Mitigation: Treat PNG conversion as a placeholder, verify generated images manually, and use a trusted converter when pixel-accurate output is required. <br>
Risk: Local scripts write to user-specified output paths and could overwrite existing files. <br>
Mitigation: Choose output paths deliberately and review target filenames before running generation or conversion commands. <br>
Risk: Node dependencies such as canvas may be needed for conversion workflows. <br>
Mitigation: Install dependencies only from trusted package sources and keep the execution environment local and scoped to the asset-generation task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NimaChu/svg-generator-pro) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated artifacts are SVG files and simplified PNG outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated visuals should be reviewed before use, especially converted PNG outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
