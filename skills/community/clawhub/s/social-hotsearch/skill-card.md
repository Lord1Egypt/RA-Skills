## Description: <br>
社媒热搜助手 helps agents query hot-search lists and analyze social-media discussion across Weibo, Xiaohongshu, Douyin, Zhihu, and Baidu for topic discovery, brand monitoring, PR review, media evaluation, and social listening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supermalo](https://clawhub.ai/user/supermalo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketing, PR, media buying, content operations, and research users can use this skill to find trending social topics, measure topic volume and sentiment, compare platform distribution, and sample public posts for qualitative context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search topics, brand names, dates, and analysis parameters are sent to an external social-media analytics proxy. <br>
Mitigation: Use the skill only for queries that fit the provider trust model; avoid confidential, unreleased, or sensitive PR and brand investigations unless external processing is approved. <br>
Risk: The skill creates a persistent local quota identity at ~/.config/social-hotsearch/user.json using a hashed machine fingerprint. <br>
Mitigation: Inform users that a local quota identity is stored and manage or remove that file according to the organization's endpoint and privacy policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/supermalo/social-hotsearch) <br>
- [Skill README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Social Skill Proxy MCP Endpoint](https://47-103-200-210.nip.io/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with shell commands and selected JSON fields from the social-media analytics scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hot-list entries, topic volume, sentiment, interaction metrics, platform distribution, related topic clusters, sampled post metadata, quota status, and user-facing error guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
