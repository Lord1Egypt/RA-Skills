## Description: <br>
Meta-skill for creating publication-ready scientific figures with multi-panel layouts, significance annotations, error bars, colorblind-safe palettes, and journal-specific formatting for Matplotlib, Seaborn, and Plotly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxr191202](https://clawhub.ai/user/yxr191202) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, researchers, and analysts use this skill to create or improve publication-ready scientific figures with journal-specific formatting, accessibility-oriented palettes, statistical annotations, and export settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or helper-script export commands can overwrite existing figure files if filenames or output folders collide. <br>
Mitigation: Use explicit output directories and filenames, and review paths before running export helpers. <br>
Risk: Generated plotting code depends on local Python plotting libraries and referenced style files being available and trusted. <br>
Mitigation: Install dependencies from trusted sources and verify referenced style files before use. <br>


## Reference(s): <br>
- [Publication-Ready Figure Guidelines](references/publication_guidelines.md) <br>
- [Scientific Color Palettes and Guidelines](references/color_palettes.md) <br>
- [Journal-Specific Figure Requirements](references/journal_requirements.md) <br>
- [Publication-Ready Matplotlib Examples](references/matplotlib_examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets, configuration recommendations, and local figure-export instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local figure files when an agent runs generated plotting or export code.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
