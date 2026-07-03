## Description: <br>
Generates and composes SVG symbols from built-in Font Awesome characters or user-provided SVG files, with sequence, permutation, combination, limited-length, batch, and preview workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to create composed SVG text, icons, badges, logo elements, and batch-generated symbol combinations for local asset workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Large permutation or Cartesian-product batch jobs can create many SVG files and consume local compute or storage. <br>
Mitigation: Keep batch inputs and length limits small, estimate output counts before running batch modes, and review the output directory before execution. <br>
Risk: Generated preview HTML may contain active SVG content or local file paths. <br>
Mitigation: Avoid opening preview HTML from untrusted SVG inputs and do not share generated preview HTML unless local paths and embedded SVG content have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/svg-composer) <br>
- [Publisher profile](https://clawhub.ai/user/ldxs001) <br>
- [Font Awesome Free license](https://fontawesome.com/license/free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, SVG strings and files, and optional preview HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include many generated SVG files in batch modes and preview HTML containing local file links.] <br>

## Skill Version(s): <br>
3.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
