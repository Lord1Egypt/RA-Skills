## Description: <br>
Generate practical UI design systems and starter pages using local style/color/typography datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dalomeve](https://clawhub.ai/user/Dalomeve) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, designers, and product teams use this skill to plan landing pages or dashboards, select style, color, and typography choices from bundled datasets, and generate starter UI files when implementation is requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate or overwrite starter UI files when implementation is requested. <br>
Mitigation: Specify the intended output folder before generation and confirm overwrites before allowing file changes. <br>
Risk: The artifact references a PowerShell helper, but the scanned file list does not include that script. <br>
Mitigation: Do not run any PowerShell helper unless the actual script is present and reviewed. <br>
Risk: Generated UI guidance can still be incorrect or mismatched to product needs even when the scan verdict is clean. <br>
Mitigation: Review generated design tokens, accessibility choices, and file paths before using the output in a project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Dalomeve/ui-design-optimizer) <br>
- [Dalomeve publisher profile](https://clawhub.ai/user/Dalomeve) <br>
- [UI-UX Pro Max source credit](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) <br>
- [UI-UX Pro Max website](https://uupm.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown design specifications with optional HTML/CSS files and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected dataset rows or slugs and generated file paths when implementation is requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
