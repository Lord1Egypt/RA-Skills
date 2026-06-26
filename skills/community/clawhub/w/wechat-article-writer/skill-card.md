## Description: <br>
公众号写作助手，支持从选题、标题、框架、成稿、Markdown 保存到配图提示词与可选图片生成的完整流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengbabao0929](https://clawhub.ai/user/fengbabao0929) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators, marketing operators, and individual publishers use this skill to plan and draft Chinese WeChat public-account articles, generate title options, structure long-form posts, and prepare matching image prompts. It also supports optional image generation after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes a bundled API key for image generation. <br>
Mitigation: Revoke or remove the bundled credential before use and configure a user-owned API key through secure local configuration. <br>
Risk: The workflow can automatically save articles and image-prompt files to a local path. <br>
Mitigation: Review and change the save directory before use, and confirm writes before allowing the workflow to create files. <br>
Risk: The optional image-generation script can execute code, call an external API, and download generated image files. <br>
Mitigation: Run the script only after explicit user approval, review the prompt input file, and verify the output directory and network/API configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengbabao0929/wechat-article-writer) <br>
- [Zhipu AI Open Platform](https://open.bigmodel.cn/) <br>
- [Publisher profile](https://clawhub.ai/user/fengbabao0929) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Conversational guidance, Markdown article drafts, saved Markdown files, image prompts, JSON or JSONL image-generation requests, and optional generated image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets 2500-3000 character Chinese articles, produces 5-10 title options, and may save article and image-prompt files to a configured local directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
