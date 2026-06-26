## Description: <br>
Scrape documentation content from Zoomin Software portals using Playwright browser automation to handle dynamic content loading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[recklessop](https://clawhub.ai/user/recklessop) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and documentation engineers use this skill to scrape rendered text from dynamic Zoomin Software documentation portals when static HTTP fetching misses the main article content. It can also summarize and categorize scraped text files for downstream documentation review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scraper performs browser-based network requests and writes extracted documentation content to local output paths. <br>
Mitigation: Run it in a dedicated virtual environment, review the URL list before scraping, and choose a non-sensitive output directory. <br>
Risk: The batch analyzer reads local text files and prints summaries to stdout. <br>
Mitigation: Do not pass private or sensitive files to the analyzer unless stdout capture and retention are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/recklessop/zoomin-scraper-recklessop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus scraped text files and JSON summaries when scripts are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a URL list, an output directory, and a Python virtual environment with Playwright and Chromium installed.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
