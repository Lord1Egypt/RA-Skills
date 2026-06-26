## Description: <br>
微信公众号内容工作室 — 支持多来源权威搜索、多站点文章抓取、AI 改写、封面生成、智能排版发布的一站式工具 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[love254443233](https://clawhub.ai/user/love254443233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and agents use this skill to research topics, collect source articles, rewrite and format WeChat public-account drafts, generate cover images, and prepare drafts for publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create WeChat drafts or publish-path outputs before a human has reviewed the generated article. <br>
Mitigation: Use --no-auto or --no-publish until the article, formatting, cover image, and target account are reviewed; supervise any browser-based publishing step. <br>
Risk: The skill uses stored API keys and may use real browser profiles for publication workflows. <br>
Mitigation: Use a task-specific .env file with least-privileged credentials, avoid real browser profiles unless actively supervising, and rotate credentials after testing or shared use. <br>
Risk: Search, rewriting, image generation, and publishing steps can send prompts, article text, URLs, or account identifiers to external services. <br>
Mitigation: Do not process confidential or embargoed material unless those service uses are approved, and review outputs for accuracy, copyright, and account-policy compliance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/love254443233/wechat-content-studio) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [WorkBuddy WebSearch integration workflow](artifact/scripts/search/workbuddy_search_workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown article files, rewritten draft files, JSON metadata, generated cover-image files, and command-line status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create drafts through WeChat publishing paths and may write outputs under the configured WorkBuddy output directory.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata and SKILL.md frontmatter; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
