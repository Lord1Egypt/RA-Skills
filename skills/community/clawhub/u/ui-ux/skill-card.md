## Description: <br>
Searchable UI/UX design databases and a Python CLI that generate design-system recommendations from natural language queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and designers use this skill to choose UI styles, color palettes, typography, chart patterns, accessibility rules, and stack-specific implementation guidance for web and app interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional persistence mode can create local Markdown files in a chosen output directory. <br>
Mitigation: Use --persist only when local design-system files are intended, keep --output-dir inside the project, and avoid project or page names that contain slashes, dot-dot paths, or path-like text. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wpank/ui-ux) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown and terminal text with optional JSON output from the search CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local design-system Markdown files when persistence is explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
