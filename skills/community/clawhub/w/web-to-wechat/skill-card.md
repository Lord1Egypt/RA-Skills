## Description: <br>
Web to WeChat helps an agent scrape web article content, clean and reformat it for WeChat, generate and compress a cover image, and create a WeChat Official Account draft. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lutongsuo](https://clawhub.ai/user/lutongsuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to turn a source URL into a cleaned Markdown article, WeChat-compatible HTML, compressed cover image, and WeChat draft for final review and publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WeChat Official Account credentials and can create drafts through the publishing workflow. <br>
Mitigation: Store WeChat secrets carefully, run the skill only in a controlled environment, and review the generated article before allowing draft creation. <br>
Risk: The bundled scripts can install Python packages at runtime if dependencies are missing. <br>
Mitigation: Preinstall and pin required dependencies in a managed environment, and avoid runtime auto-installation where package provenance is not controlled. <br>
Risk: Republishing scraped web content can carry attribution, copyright, or source-quality issues. <br>
Mitigation: Preserve source links and author credits, choose summary or rewrite modes when appropriate, and perform human review before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lutongsuo/skills/web-to-wechat) <br>
- [Publisher profile](https://clawhub.ai/user/lutongsuo) <br>
- [WeChat Official Accounts platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON extraction output, WeChat-compatible HTML, image files, and command-line instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires companion skills for Markdown-to-WeChat HTML conversion and WeChat draft publishing; generated drafts should be reviewed before publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
