## Description: <br>
Visual editor for HTML presentations. Self-contained, offline-capable, designed for AI agent control. HTML 演示文稿可视化编辑器，自包含可离线，支持 AI Agent 控制。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DTacheng](https://clawhub.ai/user/DTacheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inject a browser-based editor into HTML presentations, manipulate slide elements visually or through a JavaScript API, and export clean or editor-enabled HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recommended workflow rewrites local HTML presentation files. <br>
Mitigation: Run the injector against a copy of the presentation and review the exported HTML before replacing original files. <br>
Risk: The injector can execute local shell commands to open files in a browser. <br>
Mitigation: Avoid the --open option for untrusted or unusually named files until the shell execution path has been reviewed and hardened. <br>
Risk: The editor exposes broad browser-global editing controls. <br>
Mitigation: Use the editor only on presentations you intend to modify and inspect exported files before sharing or deploying them. <br>
Risk: The documentation includes curl pipe-to-shell and PowerShell installer commands for Bun. <br>
Mitigation: Install Bun through a trusted, independently verified method before running the skill workflow. <br>


## Reference(s): <br>
- [ClawHub Slide Editor listing](https://clawhub.ai/DTacheng/slide-editor) <br>
- [Bun runtime](https://bun.sh) <br>
- [Bun install documentation](https://bun.sh/install) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JavaScript examples; generated or rewritten HTML presentation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can inject the editor inline or as a linked bundle, open the edited presentation in a browser, and export clean HTML without editor artifacts.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
