## Description:

Meta-skill for publication-ready figures. Use when creating journal submission figures requiring multi-panel layouts, significance annotations, error bars, colorblind-safe palettes, and specific journal formatting (Nature, Science, Cell). Orchestrates matplotlib/seaborn/plotly with publication styles. For quick exploration use seaborn or plotly directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxr191202](https://clawhub.ai/user/yxr191202)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and scientific authors use this skill to create and refine publication-ready figures, including multi-panel plots, statistical annotations, accessible color palettes, journal-specific formatting, and PDF/EPS/TIFF exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Figure exports and style-template generation may overwrite existing files when reused filenames or output paths are provided.

Mitigation: Use explicit output directories and review filenames before allowing the agent to export figures or create style templates.

Risk: The skill operates on local data and output paths supplied during use.

Mitigation: Limit use to datasets and directories the agent is intended to access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yxr191202/skills/scientific-visualization)
- [Scientific Color Palettes and Guidelines](references/color_palettes.md)
- [Journal-Specific Figure Requirements](references/journal_requirements.md)
- [Publication-Ready Matplotlib Examples](references/matplotlib_examples.md)
- [Publication-Ready Figure Guidelines](references/publication_guidelines.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code snippets and publication figure export recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify local figure files and matplotlib style files at paths selected by the user.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
