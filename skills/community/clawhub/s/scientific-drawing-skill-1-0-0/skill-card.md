## Description: <br>
基于 AutoFigure-Edit 的科研级科学插图生成与编辑系统，能够从长篇方法描述自动生成完全可编辑的矢量图（SVG），支持参考图风格迁移和浏览器内交互式编辑 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidzhao30](https://clawhub.ai/user/davidzhao30) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical writers use this skill to turn method descriptions into editable scientific figures, including SVG outputs, style-guided variants, and browser-editable diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses external AI providers and API keys, so confidential unpublished research may be sent outside the local environment depending on provider configuration. <br>
Mitigation: Keep API keys scoped and avoid submitting confidential research unless the selected provider terms and data handling are acceptable. <br>
Risk: The documented editor/server behavior can expose generated files or uploads if bound to a network interface unintentionally. <br>
Mitigation: Run the editor in an isolated Python environment and bind it to localhost unless broader network access is intentional. <br>
Risk: The workflow depends on an external AutoFigure-Edit repository and Python dependencies that are outside the reviewed documentation artifact. <br>
Mitigation: Review the external repository and dependencies before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidzhao30/scientific-drawing-skill-1-0-0) <br>
- [AutoFigure-Edit project](https://github.com/ResearAI/AutoFigure-Edit) <br>
- [Gemini API documentation](https://ai.google.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with command examples and generated SVG, PNG, JSON, and image asset files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include editable SVG figures, rendered PNG previews, segmentation metadata, templates, and extracted icon assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
