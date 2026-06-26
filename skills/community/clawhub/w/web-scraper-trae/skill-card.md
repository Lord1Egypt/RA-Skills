## Description: <br>
Opens browser and scrapes webpage content using Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengjia626](https://clawhub.ai/user/zhengjia626) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create and run a Playwright-based Node.js scraper for authorized URLs, returning page title, visible text, full HTML, and the source URL as JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scraped output can expose page text and full HTML from user-provided URLs. <br>
Mitigation: Use the skill only on public or clearly authorized pages, and avoid confidential, authenticated, or intranet content unless the agent is allowed to receive it. <br>
Risk: Untrusted pages may behave unexpectedly during browser automation. <br>
Mitigation: Run scraping in an isolated environment and review target URLs before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhengjia626/web-scraper-trae) <br>
- [Publisher profile](https://clawhub.ai/user/zhengjia626) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples; scraper results are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scraper returns title, visible text, full HTML, and the original URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
