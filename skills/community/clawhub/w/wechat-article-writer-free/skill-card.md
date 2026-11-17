## Description: <br>
Generates WeChat public-account article drafts from topics or outlines and supports basic polishing, rewriting, continuation, titles, summaries, and article structures for individual creators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External individual creators use this skill to turn topics or outlines into WeChat public-account article drafts, then polish, rewrite, continue, title, and summarize the content before publication review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or modify local article draft or configuration files. <br>
Mitigation: Confirm target filenames and paths, especially draft.md and configuration files, before saving or overwriting content. <br>
Risk: Optional external model API keys or command-line helper steps can expand exposure beyond the core Markdown workflow. <br>
Mitigation: Use the built-in agent writing path when possible, avoid unnecessary external keys, and review any command-line helper steps before execution. <br>
Risk: Generated article drafts may contain inaccurate claims or may not match the intended publication voice. <br>
Mitigation: Review factual claims, tone, and publication suitability before publishing or reusing the draft. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/wechat-article-writer-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown article drafts with optional YAML or Python configuration examples and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local draft or configuration files such as draft.md, config.yaml, article.yaml, or .article/config.yaml when the agent follows save/export guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
