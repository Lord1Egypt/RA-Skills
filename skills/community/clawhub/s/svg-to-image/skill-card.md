## Description: <br>
Convert SVG to PNG or JPG for quick sharing (e.g. Telegram) or print. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QROST](https://clawhub.ai/user/QROST) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, designers, and external OpenClaw users can use this skill to rasterize SVG diagrams, maps, or vector graphics into PNG or JPG files for chat, documents, or print. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local SVG conversion runs a Python renderer on user-selected files, so untrusted SVG content or stale dependencies can increase execution and parsing risk. <br>
Mitigation: Use trusted SVG files and keep cairosvg, Pillow, and the system Cairo library current or pinned according to the deployment environment. <br>
Risk: Ambiguous input or output paths can write files to an unexpected location or prevent media delivery. <br>
Mitigation: Use explicit input paths and write shareable outputs to allowed media locations such as /tmp or ~/.openclaw/media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QROST/svg-to-image) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG or JPG image files with concise terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports optional output path, image format, width, height, and DPI settings.] <br>

## Skill Version(s): <br>
1.1.1 (source: SKILL.md frontmatter, clawhub.json, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
