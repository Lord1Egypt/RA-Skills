## Description: <br>
Scans web-novel ranking data from Qidian, Fanqie, JJWXC, Qimao, and Ciweimao to identify long-form fiction market trends and topic opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authors, editors, and fiction market researchers use this skill to gather or inspect ranking samples, compare platform-specific reader signals, and produce actionable topic candidates with validation steps for long-form web novels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact public fiction ranking sites and optionally control a Chrome/CDP browser during scraping. <br>
Mitigation: Run it only where this web access is acceptable, and use a dedicated browser profile if scraping should stay separate from personal browsing. <br>
Risk: The scripts write Markdown reports to local output directories. <br>
Mitigation: Choose a specific output directory and review generated reports before relying on or sharing them. <br>


## Reference(s): <br>
- [Genre Trends Reference](references/genre-trends.md) <br>
- [Publishing Guide](references/publishing-guide.md) <br>
- [Reader Profiling Reference](references/reader-profiling.md) <br>
- [Scan Output Format](references/scan-output-format.md) <br>
- [Topic Decision Reference](references/topic-decision.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, tables, shell command examples, and local Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scraper outputs are written to a user-selected output directory; some collection paths may use public web access or a Chrome/CDP browser session.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
