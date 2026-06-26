## Description: <br>
生成适合视频号发布的爆款IP内容方案：选题、标题、钩子、口播脚本、镜头建议、封面文案、发布文案、评论引导，以及医美场景下的基础合规改写。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangfu20171212-hue](https://clawhub.ai/user/yangfu20171212-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, medical-aesthetics operators, and personal-brand teams use this skill to produce structured WeChat Channels topic ideas, scripts, style rewrites, and compliance-oriented safer copy for publishable Chinese video content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and user-provided content may be sent to the configured model endpoint. <br>
Mitigation: Use a trusted model endpoint, use MODEL_MOCK_RESPONSE for offline testing, and avoid including unrelated secrets in CLI input files. <br>
Risk: Medical-aesthetics marketing copy may contain compliance-sensitive claims even after generation. <br>
Mitigation: Run the compliance action and apply human review before publishing content that mentions medical-aesthetics services or expected outcomes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangfu20171212-hue/video-wechat-ip-script-agent) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [README](artifact/README.md) <br>
- [Developer README](artifact/README-DEV.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON or Markdown with command examples, depending on the selected action and invocation mode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports topic generation, full script packages, style rewrites, and compliance review outputs; can use MODEL_MOCK_RESPONSE for offline validation.] <br>

## Skill Version(s): <br>
1.3.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
