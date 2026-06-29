## Description: <br>
帮助小程序商家、运营团队和开发者选择微信小程序 AI 接入模式，并生成结构化数据清单、开发模式草案、代码骨架、测试矩阵和上线检查。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangjihua007-rgb](https://clawhub.ai/user/huangjihua007-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External merchants, operations teams, and developers use this skill to assess WeChat Mini Program AI integration paths, structure product and service data for AI use, and draft implementation assets for development mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scaffolds may contain placeholder server URLs or generic business logic that is not ready for production use. <br>
Mitigation: Review all generated files, replace placeholders with real service endpoints and business rules, and test the implementation before relying on it. <br>
Risk: The referenced WeChat Mini Program AI development mode is described as beta-stage with code review not yet open. <br>
Mitigation: Keep beta-stage cautions visible, do not merge generated development-mode code into a formal release until the platform review path is available, and validate against current WeChat requirements. <br>
Risk: Advice touching payment, privacy data, user confirmation, or content safety can affect compliance and user trust. <br>
Mitigation: Retain explicit user confirmation, privacy authorization, payment, and content safety checks, and have responsible reviewers approve workflows before launch. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangjihua007-rgb/skills/wechat-aiagent-dev) <br>
- [README](README.md) <br>
- [微信小程序 AI 入门与接入模式](references/wechat-agent-basics.md) <br>
- [微信小程序 AI 开发模式 · 能力清单](references/ai-capabilities.md) <br>
- [行业接入示范](references/industry-cases.md) <br>
- [GEO 数据、测试与上线清单](references/geo-checklists.md) <br>
- [开发模式三件套模板](references/dev-mode-templates.md) <br>
- [代码生成模板](references/code-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tables and code/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory drafts and code skeletons that require user review, replacement of placeholder service URLs, and validation against WeChat Mini Program AI beta constraints before use.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
