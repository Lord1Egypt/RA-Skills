## Description: <br>
Automates Xiaohongshu workflows for login, content publishing, content discovery, social interaction, and multi-step content operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengfan-ai](https://clawhub.ai/user/zengfan-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Xiaohongshu through an agent, including checking login status, publishing posts, searching and analyzing notes, commenting, liking, favoriting, and coordinating content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give a local browser extension and Python bridge broad control over a logged-in Xiaohongshu browser session. <br>
Mitigation: Install only after reviewing the extension permissions and run it with a dedicated account or browser profile where possible. <br>
Risk: Automated posts, comments, likes, and favorites can affect a real social account and may trigger platform enforcement if used too quickly. <br>
Mitigation: Require review before every post, comment, like, or favorite action and keep operation frequency low. <br>
Risk: Login flows and cookie handling involve sensitive account state. <br>
Mitigation: Avoid the QR login flow unless the browser bridge permissions are understood, and clear stored cookies when switching or retiring accounts. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zengfan-ai/xhs-skills) <br>
- [Metadata homepage](https://github.com/xpzouying/xiaohongshu-skills) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI operations return structured JSON; analysis workflows may return markdown tables and summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata, release evidence, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
