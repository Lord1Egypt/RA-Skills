## Description: <br>
Helps an agent perform lightweight, user-directed analysis of public Xiaohongshu notes and creator profile pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to summarize public Xiaohongshu search results, topics, notes, and creator-profile content for lightweight trend and performance analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Use for bulk scraping, platform-control bypass, downloading content, or automatic account actions could violate the documented release boundaries. <br>
Mitigation: Limit use to small, user-directed analysis of public pages and do not perform downloads, reverse engineering, bulk collection, or account actions. <br>
Risk: Logged-in browsing may expose account-specific page context to the agent. <br>
Mitigation: Prefer public-page review where possible and avoid sharing sensitive account state or private content during analysis. <br>
Risk: Dynamic pages and human checks can make extracted engagement metrics incomplete or stale. <br>
Mitigation: Treat outputs as lightweight summaries and verify important findings against the live Xiaohongshu page before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/xiaohongshu-hot-trend) <br>
- [Xiaohongshu homepage](https://www.xiaohongshu.com/) <br>
- [Xiaohongshu explore page](https://www.xiaohongshu.com/explore) <br>
- [Xiaohongshu search page](https://www.xiaohongshu.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or concise text summaries with analysis notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include summarized engagement metrics, topic/category distributions, creator-profile comparisons, and compliance reminders.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
