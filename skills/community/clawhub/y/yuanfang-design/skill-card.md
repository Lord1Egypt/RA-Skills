## Description: <br>
Shared design system for yuanfang-skills that provides token CSS variables, themes, and reusable layout-type HTML blocks for visually consistent output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iyuanfang](https://clawhub.ai/user/iyuanfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-tool authors use this skill to add or maintain reusable themes, layout blocks, and design tokens for Yuanfang HTML/image generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The showcase generator writes generated preview files locally and expects a neighboring yuanfang-html-image project. <br>
Mitigation: Run the showcase in a development workspace where local generated files are expected, and confirm the neighboring renderer project is present before using that workflow. <br>
Risk: Theme or layout changes can reduce visual consistency or readability if token rules are bypassed. <br>
Mitigation: Follow the bundled authoring guide and run the provided token and registry tests before release. <br>


## Reference(s): <br>
- [Yuanfang Design Authoring Guide](references/authoring-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CSS, HTML, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for local design-system files and theme/layout authoring workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
