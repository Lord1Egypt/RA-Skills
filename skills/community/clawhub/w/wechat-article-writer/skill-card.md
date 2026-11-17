## Description:

A WeChat public-account writing assistant that guides an agent from topic selection through title options, outline, full Markdown draft, saved article files, image prompts, and optional image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengbabao0929](https://clawhub.ai/user/fengbabao0929)

### License/Terms of Use:


## Use Case:

External users and content creators use this skill to produce WeChat public-account articles with staged topic refinement, title selection, article structure, full Markdown drafting, and associated image prompts. Developers may also use its bundled script and configuration pattern to generate article images through a Zhipu AI image API after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package ships a plaintext image API key.

Mitigation: Remove the bundled key, rotate the exposed credential, and require each user to configure their own API key before installation or use.

Risk: The skill automatically writes article and image-prompt files to a configured local directory.

Mitigation: Review the destination path before use and add overwrite or confirmation controls for file writes in shared or production environments.

Risk: The image-generation helper depends on a network API and Python SDK configuration.

Mitigation: Use the documented SDK, pin the dependency version before broad deployment, and keep image generation behind explicit user confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengbabao0929/skills/wechat-article-writer)
- [Zhipu AI Open Platform](https://open.bigmodel.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown articles, Markdown image prompts, JSON or JSONL image requests, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets 2500-3000 Chinese characters for full articles and can save Markdown article and image-prompt files to a configured local directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
