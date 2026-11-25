## Description:

Scientific Drawing helps agents create research diagrams, including technical roadmaps, flowcharts, schematics, architecture diagrams, Gantt charts, and data visualizations, using Python matplotlib/Pillow with high-resolution PNG and SVG output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, grant writers, academic authors, and supporting developers use this skill to turn diagram requirements into Python-generated figures for proposals and papers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated drawing helpers write image files to fixed or caller-controlled filesystem paths.

Mitigation: Run the skill in a workspace or sandbox and validate or constrain output paths before executing generated or helper code.

Risk: Figure-generation code depends on local fonts and platform-specific output paths.

Mitigation: Confirm required fonts and redirect output to a controlled project directory before relying on generated figures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jirboy/skills/scientific-drawing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python code and generated PNG/SVG/PDF figure files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default figure output is 300 DPI; helper scripts use matplotlib/Pillow and a fixed local output directory unless adjusted.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
