## Description: <br>
Generate and preview CSS shadow effects using CLI tools for box-shadow, text-shadow, drop-shadow, layered shadows, presets, animations, and export workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to generate, save, preview, animate, and export CSS shadow values for interface design and design-system work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Bash/Python CLI and may write saved presets under ~/.shadow/data.jsonl. <br>
Mitigation: Review the script before installation and use save options only when local preset storage is expected. <br>
Risk: HTML preview generation can write to a user-supplied output path. <br>
Mitigation: Confirm the --output path before generating preview files to avoid overwriting unintended files. <br>


## Reference(s): <br>
- [Shadow on ClawHub](https://clawhub.ai/bytesagain-lab/shadow) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output, CSS/JSON/SCSS exports, and optional HTML preview files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saved presets are written to ~/.shadow/data.jsonl when save options are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
