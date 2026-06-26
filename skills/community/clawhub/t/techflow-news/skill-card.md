## Description: <br>
techflow-news gathers same-day TechFlow articles and produces a table of dates, article titles, summaries, URLs, plus a short topic summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yejiming](https://clawhub.ai/user/yejiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer prompts such as today's news or today's article roundup by collecting same-day Chinese TechFlow posts, separating in-depth articles from 7x24h updates, and returning a concise summary with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is scoped to Chinese TechFlow-only news and can miss broader market or multilingual coverage. <br>
Mitigation: Use it when TechFlow-only coverage is intended; ask the agent to add other sources or languages for broader news coverage. <br>
Risk: Same-day filtering and article extraction may be incomplete if the source site changes layout or publishes relative links unexpectedly. <br>
Mitigation: Check returned dates and source URLs before relying on the summary, especially for time-sensitive decisions. <br>


## Reference(s): <br>
- [TechFlow source site](https://www.techflowpost.com/?lang=zh-CN) <br>
- [ClawHub skill page](https://clawhub.ai/yejiming/techflow-news) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown table followed by a concise prose summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes article date, title, main-content summary, complete URL, and 3-5 core news highlights.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
