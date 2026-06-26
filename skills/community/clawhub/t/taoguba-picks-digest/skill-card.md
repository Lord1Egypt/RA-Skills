## Description: <br>
自动抓取淘股吧“今日推荐”前N个帖子内容，并整理整体行情、板块表现、多数作者观点和焦点个股。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guowei-xie](https://clawhub.ai/user/guowei-xie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and market-watch agents use this skill to collect Taoguba 今日推荐 posts and produce a concise A-share market review. It helps summarize market conditions, sector strength, common author viewpoints, and repeatedly mentioned stocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use Taoguba credentials supplied through environment variables to sign in and fetch posts. <br>
Mitigation: Use a dedicated or low-risk Taoguba account, avoid reusing important passwords, and remove TAOGUBA_USERNAME and TAOGUBA_PASSWORD after use if future automatic login is not desired. <br>
Risk: The digest reflects viewpoints collected from Taoguba posts and may not be complete or investment advice. <br>
Mitigation: Review the cited post content and treat the output as a summary of author opinions rather than an independent market recommendation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guowei-xie/taoguba-picks-digest) <br>
- [Taoguba website](https://www.tgb.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown market digest with optional tables and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes collected post content objectively and avoids storing Taoguba credentials in files or logs.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
