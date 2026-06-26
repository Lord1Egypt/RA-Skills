## Description: <br>
Analyzes short-form Chinese web fiction ranking samples and platform data to identify market signals, emotional hooks, topic opportunities, saturation risks, and follow-up validation actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and market analysts use this skill to scan short-form web fiction platforms, compare ranking samples, and turn fast-changing market signals into story direction candidates and validation plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate collection from a logged-in Heiyan management backend by reusing a browser session token. <br>
Mitigation: Use public-data workflows by default; run authenticated collection only with explicit authorization, scoped accounts, and review of the data collection purpose. <br>
Risk: Market conclusions can become stale because short-form fiction trends change quickly. <br>
Mitigation: Include the sample date, trend confidence, and next rescan time before relying on topic or emotional-direction recommendations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/worldwonderer/story-short-scan) <br>
- [OpenClaw source metadata](https://github.com/worldwonderer/oh-story-claudecode) <br>
- [Short-form web fiction market reference](references/real-market-data.md) <br>
- [Dianzhong browse data source](https://www.ishugui.com/browse) <br>
- [Heiyan management book list data source](https://manage.zhangwenpindu.cn/books/booklist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown market scan report with tables, ranked findings, risk notes, and optional scraper command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on user-provided data, public platform pages, or browser/CDP collection; authenticated backend collection should be used only when explicitly authorized.] <br>

## Skill Version(s): <br>
1.1.5 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
