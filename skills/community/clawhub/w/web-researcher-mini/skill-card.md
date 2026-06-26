## Description: <br>
Web Researcher Mini helps agents search, scrape, crawl, and summarize web content into clean Markdown or JSON for research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weilianglin100-sketch](https://clawhub.ai/user/weilianglin100-sketch) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to collect web pages, crawl sites, search the web, and summarize URLs or files for research, documentation extraction, competitive intelligence, and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External scraping and AI summarization services can receive submitted URLs, documents, page content, and configured API credentials. <br>
Mitigation: Use approved public or shareable content only, avoid secrets and private/internal URLs unless approved, and configure scoped API keys. <br>
Risk: Broad searches, crawls, or parallel scraping jobs can consume Firecrawl credits or collect more pages than intended. <br>
Mitigation: Check status and credits first, confirm crawl limits, depth, concurrency, include/exclude paths, and output destinations before broad jobs. <br>
Risk: Setup and workflow steps may add .firecrawl outputs to .gitignore or suggest shell-profile changes for API keys. <br>
Mitigation: Review .gitignore and shell-profile changes before accepting them, and avoid committing generated research outputs or credentials. <br>


## Reference(s): <br>
- [Web Researcher Mini ClawHub listing](https://clawhub.ai/weilianglin100-sketch/web-researcher-mini) <br>
- [Summarize homepage](https://summarize.sh) <br>
- [Firecrawl CLI installation guidance](artifact/firecrawl-skills/rules/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; Firecrawl and summarize commands can produce Markdown, JSON, text, HTML, links, screenshots, or extracted summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write extracted or summarized results to local files such as .firecrawl outputs when directed by the agent workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
