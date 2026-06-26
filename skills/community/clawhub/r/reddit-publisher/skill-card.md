## Description: <br>
Researches subreddits, drafts Reddit-native posts, and publishes or schedules them through Late API with ScrapeCreators-based Reddit reading and an anti-AI-slop drafting pass. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nirusan](https://clawhub.ai/user/nirusan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and operators use this skill to research Reddit communities, draft subreddit-aware posts, and publish or schedule reviewed posts through a connected Late/Reddit account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or schedule Reddit posts through a connected Late/Reddit account. <br>
Mitigation: Manually review the account, subreddit, title, body, flair, and schedule before every posting command. <br>
Risk: The skill includes guidance to make AI-written posts sound human. <br>
Mitigation: Follow subreddit disclosure and promotion rules, and avoid using the drafting workflow to misrepresent identity or intent. <br>
Risk: The workflow depends on ScrapeCreators and Late API keys. <br>
Mitigation: Store keys only in the documented environment variables or config files, restrict file permissions, and rotate keys if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skills/reddit-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/nirusan) <br>
- [ScrapeCreators](https://scrapecreators.com) <br>
- [Late](https://getlate.dev) <br>
- [Stop-slop phrases reference](references/stop-slop/phrases.md) <br>
- [Stop-slop structures reference](references/stop-slop/structures.md) <br>
- [Stop-slop examples reference](references/stop-slop/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON returned by helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCRAPECREATORS_API_KEY and LATE_API_KEY or matching local config files for API-backed workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
