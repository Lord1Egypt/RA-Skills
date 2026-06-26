## Description: <br>
快速创建 Remotion 视频项目的技能。提供完整的项目模板、动画工具函数、渲染脚本和最佳实践。一键创建专业视频项目。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bozoyan](https://clawhub.ai/user/bozoyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video creators use this skill to scaffold Remotion projects, apply reusable animation patterns, configure rendering commands, and produce video outputs such as MP4, WebM, or GIF files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud-rendering commands may create cloud resources, incur costs, or use sensitive credentials if run without review. <br>
Mitigation: Treat Lambda or other cloud-rendering steps as optional advanced workflows; use least-privilege credentials, non-sensitive test media, and explicit cost controls. <br>
Risk: Project creation commands install npm dependencies and write files into the chosen project directory. <br>
Mitigation: Run setup commands in an isolated workspace, review generated package scripts and configuration, and inspect dependency changes before using the project for production work. <br>


## Reference(s): <br>
- [Remotion documentation](https://www.remotion.dev/docs) <br>
- [Project template rules](rules/project-template.md) <br>
- [Animation tool rules](rules/animation-tools.md) <br>
- [Rendering rules](rules/rendering.md) <br>
- [Chrome reuse rules](rules/chrome-reuse.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and TypeScript or JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Remotion project files and video render outputs when the user runs the provided commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
