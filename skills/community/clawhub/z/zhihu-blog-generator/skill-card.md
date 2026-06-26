## Description: <br>
知乎风格技术博客生成器 - 自动化生成高质量技术文章 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xieyuantao7](https://clawhub.ai/user/xieyuantao7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to select or provide a technical topic, collect supporting sources, draft a Zhihu-style technical blog post, refine the prose, and output a publishable Markdown article. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided topic text can be passed through shell-driven commands. <br>
Mitigation: Review topic strings before running one-click workflows and avoid executing commands with untrusted or unsanitized input. <br>
Risk: Generated posts can contain publishable-looking technical claims, metrics, case studies, source-code analysis, or personal-experience statements that are not source-backed. <br>
Mitigation: Fact-check every generated claim against collected sources before publishing and require human editorial review for final Markdown output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xieyuantao7/zhihu-blog-generator) <br>
- [Publisher profile](https://clawhub.ai/user/xieyuantao7) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles, JSON workflow artifacts, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes topic, collection, draft, refinement, and final output files under the configured reports directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
