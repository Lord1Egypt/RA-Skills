## Description: <br>
Generates weekly technology news briefings from major English-language tech media RSS feeds, highlighting multi-source stories, autonomous-driving coverage, and company-specific navigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangzhe1991](https://clawhub.ai/user/yangzhe1991) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect public technology RSS items, deduplicate recent articles, identify stories covered by multiple outlets, and produce a concise weekly briefing. It is suited for monitoring English tech media coverage with source attribution and company-focused follow-up views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public news feeds and writes local article, company, and briefing files. <br>
Mitigation: Review setup, output paths, and scheduled jobs before running the scripts. <br>
Risk: Generated briefings may contain attribution or topic-filtering errors. <br>
Mitigation: Treat briefings as convenience summaries and verify important claims against the linked source articles. <br>
Risk: Setup steps can add blogwatcher feed entries or cron jobs. <br>
Mitigation: Inspect the setup and cron commands before enabling automation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yangzhe1991/tech-weekly-briefing) <br>
- [TechCrunch RSS Feed](https://techcrunch.com/feed/) <br>
- [The Verge RSS Feed](https://www.theverge.com/rss/index.xml) <br>
- [Wired RSS Feed](https://www.wired.com/feed/rss) <br>
- [Ars Technica RSS Feed](https://arstechnica.com/feed/) <br>
- [MIT Technology Review RSS Feed](https://www.technologyreview.com/feed/) <br>
- [The Information RSS Feed](https://www.theinformation.com/feed) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown-style briefing text with source links, JSON article data files, and shell commands for setup or scheduled runs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily article JSON, company categorization JSON, and weekly briefing text files; generated briefings should be treated as convenience summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and SKILL.md version history, released 2026-03-09) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
