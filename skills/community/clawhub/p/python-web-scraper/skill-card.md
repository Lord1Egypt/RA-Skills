## Description: <br>
Python web scraping toolkit for extracting website data, handling pagination and JavaScript-rendered pages, applying anti-blocking techniques, and producing structured JSON or CSV output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create or adapt Python scrapers for authorized public websites, including basic pages, pagination, JavaScript-rendered content, and JSON, CSV, or text outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes guidance for bypassing site defenses and handling login or session cookies. <br>
Mitigation: Use it only for public or clearly authorized sites, prefer official APIs, and avoid cookie/login, CAPTCHA-solving, proxy-rotation, and webdriver-bypass techniques unless explicit permission and a controlled use case exist. <br>
Risk: Selenium tooling and web driver dependencies may execute code or fetch browser driver components in the local environment. <br>
Mitigation: Review and pin Python dependencies before running Selenium workflows, and execute them in an isolated environment when possible. <br>
Risk: Scraping can collect personal, copyrighted, or terms-restricted content if configured against inappropriate targets. <br>
Mitigation: Limit targets to authorized public data, check robots.txt and site terms, apply rate limits, and avoid scraping personal data or protected content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ericlooi504/python-web-scraper) <br>
- [Anti-Blocking Strategies](references/anti-blocking.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; scraper scripts can produce JSON, CSV, or plain text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command-line scraper templates for single pages, pagination, and Selenium-based JavaScript rendering.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
