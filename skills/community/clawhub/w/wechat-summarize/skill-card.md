## Description: <br>
抓取微信公众号文章并转换为 Markdown，提取正文内容后总结核心观点或直接输出完整文章。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongym1234](https://clawhub.ai/user/kongym1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers and agents use this skill to fetch a user-provided WeChat Official Account article, convert its body to Markdown, and summarize the article's key points or return the full extracted content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted or inaccessible WeChat article links may fail to fetch, require human verification, or yield content that needs review before relying on a summary. <br>
Mitigation: Use trusted WeChat article links and review or retain the generated Markdown when an audit copy is needed. <br>
Risk: Fallback dependency installation pulls current Python package versions. <br>
Mitigation: Preinstall or pin the required Python dependencies in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kongym1234/wechat-summarize) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown article files, Markdown summaries, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated Markdown files are normally deleted after summarization unless the user asks to keep them; optional image download writes local image files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
