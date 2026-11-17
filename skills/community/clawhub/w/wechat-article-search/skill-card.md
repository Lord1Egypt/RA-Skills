## Description:

Searches WeChat public-account articles by keyword and returns article titles, summaries, publication times, source account names, and links.

This skill is for research and development only.

## Publisher:

[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018)

### License/Terms of Use:


## Use Case:

External users and researchers use this skill to search WeChat public-account articles by keyword and collect titles, summaries, dates, source account names, and links for reference gathering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scraping-style requests and optional real-URL resolution may violate site rules, trigger anti-scraping controls, or expose the running environment to unnecessary outbound requests.

Mitigation: Use the skill only for explicit, limited WeChat article searches; review applicable site terms; avoid large-scale crawling; and enable real-URL resolution only when needed.

Risk: The artifact recommends a global npm installation for the cheerio dependency, which can make dependency versions harder to review and reproduce.

Mitigation: Prefer a project-local, pinned dependency installation and review the dependency source and lockfile before running the script.

Risk: Weak URL validation can make resolved links and outbound requests more influenced by remote page content.

Mitigation: Run the skill in a constrained environment, inspect returned links before opening them, and avoid resolving real URLs unless the workflow requires it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuchubuzai2018/skills/wechat-article-search)
- [Sogou Weixin Search](https://weixin.sogou.com/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON search results and concise Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally write search results to a JSON file when the output option is used.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
