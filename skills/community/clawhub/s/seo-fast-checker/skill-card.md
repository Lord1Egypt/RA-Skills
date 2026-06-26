## Description: <br>
输入网址一键输出SEO诊断报告，检查标题/描述/Headers/关键词密度/图片alt/页面速度/移动端适配/Meta标签，输出可执行优化建议 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyjaixiao](https://clawhub.ai/user/hyjaixiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Website owners, marketers, and developers use this skill to audit public web pages for SEO metadata, headings, image alt text, links, structured data, page size, mobile viewport settings, and actionable optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional AI mode can send fetched page text to OpenAI or the configured model provider. <br>
Mitigation: Use basic non-AI mode for sensitive, internal, authenticated, confidential, client-owned, or regulated pages; enable --ai only with approval to send page content to the provider. <br>
Risk: The checker makes outbound requests to user-supplied URLs. <br>
Mitigation: Install and run it only where outbound URL scanning is approved, and avoid targets you are not authorized to inspect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hyjaixiao/seo-fast-checker) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown SEO diagnostic report with optional AI-enhanced markdown analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches supplied URLs over HTTP(S); optional --ai mode uses OPENAI_API_KEY and OPENAI_MODEL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
