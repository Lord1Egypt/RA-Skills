## Description: <br>
Adaptive web scraping framework with anti-bot bypass and spider crawling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zendenho7](https://clawhub.ai/user/zendenho7) <br>

### License/Terms of Use: <br>
BSD-3-Clause <br>


## Use Case: <br>
Developers and agents use Scrapling to fetch, parse, and crawl website content for research, summaries, brand data extraction, and structured data collection from permitted sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes bypass and API-replication guidance that could be misused on paid, protected, rate-limited, or terms-prohibited services. <br>
Mitigation: Use it only on sites where scraping is permitted, respect robots.txt and site terms, and avoid protected, paywalled, or rate-limited services unless explicitly authorized. <br>
Risk: The helper script can install packages and run local Python spider files. <br>
Mitigation: Review run.sh and any spider file before execution, use an isolated virtual environment or container, and run only trusted local files. <br>
Risk: Untrusted URLs or selectors can cause unwanted network requests or unreliable extraction results. <br>
Mitigation: Pass only reviewed URLs and selectors, limit crawl scope and concurrency, and validate scraped outputs before relying on them. <br>


## Reference(s): <br>
- [Scrapling ClawHub Page](https://clawhub.ai/zendenho7/scrapling) <br>
- [Scrapling Documentation](https://scrapling.readthedocs.io) <br>
- [Scrapling Core Library Repository](https://github.com/D4Vinci/Scrapling) <br>
- [API Reverse Engineering Methodology Repository](https://github.com/paoloanzn/free-solscan-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce scraping snippets, crawl patterns, selector examples, and helper-script commands.] <br>

## Skill Version(s): <br>
1.0.8 (source: frontmatter, release evidence, and changelog dated 2026-02-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
