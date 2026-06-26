## Description: <br>
Professional Figma design analysis and asset export for extracting design data, exporting assets, auditing accessibility compliance, analyzing design systems, and generating design documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yylgit](https://clawhub.ai/user/yylgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and design-system maintainers use this skill to inspect Figma files, export assets and design tokens, audit accessibility and style consistency, and generate handoff reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Figma token can expose any files reachable by that token. <br>
Mitigation: Use a limited or temporary token, prefer environment variables over command-line arguments, and keep .env files out of version control. <br>
Risk: Generated assets and reports can contain private design content. <br>
Mitigation: Export into a dedicated folder and review generated files before sharing or publishing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yylgit/yyl-test-skill) <br>
- [Figma API reference](artifact/references/figma-api-reference.md) <br>
- [Accessibility guidelines](artifact/references/accessibility-guidelines.md) <br>
- [Design patterns](artifact/references/design-patterns.md) <br>
- [Export formats](artifact/references/export-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON responses, HTML reports, image assets, and generated design-token files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local export folders, manifests, accessibility reports, audit reports, and design-token files from Figma data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
