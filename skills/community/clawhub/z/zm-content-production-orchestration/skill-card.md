## Description: <br>
ZM 图文内容生产编排用于公众号、小红书、抖音等图文内容的多 Agent 生产流程：选题定位、正文生产、视觉生产、审核返工、排版发布、交付包归档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, editors, and marketing teams use this skill to coordinate a Chinese multi-agent workflow for social content planning, article drafting, visual direction, review, revision, and delivery packaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated articles may include unsupported case claims if source material is missing. <br>
Mitigation: Provide real case material before execution and block claims that are not grounded in supplied sources. <br>
Risk: Image generation or publishing steps may move beyond the user's intent if not reviewed. <br>
Mitigation: Keep visual generation and publishing user-directed, and require final review before delivery or release. <br>
Risk: Generated delivery packages may be incomplete or placed in the wrong project location. <br>
Mitigation: Require a project-appropriate delivery path and verify article, cover image, preview, metadata, and checklist files before marking the task complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-content-production-orchestration) <br>
- [AI 可执行性审核表](checklists/ai_readiness_checklist.md) <br>
- [最小必填字段](templates/minimum_required_fields.md) <br>
- [SubAgent 执行提示词](templates/subagent_execution_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with local delivery package files such as article.md, preview.html, meta.json, publish-checklist.md, and cover image assets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided platform, target audience, content goal, core viewpoint, visual requirements, compliance boundary, review criteria, and delivery package path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
