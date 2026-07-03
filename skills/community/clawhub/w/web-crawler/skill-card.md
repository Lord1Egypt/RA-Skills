## Description: <br>
Generates Python web crawler and scraper guidance, scripts, setup commands, and troubleshooting steps for static sites, dynamic JavaScript-rendered pages, APIs, authenticated sessions, and multiple export formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moxin1044](https://clawhub.ai/user/moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to design and generate Python crawlers for authorized websites, including API-first crawlers, browser-based crawlers for SPAs, authenticated workflows, pagination, and export pipelines. It is intended for users who need practical crawler implementation guidance while accounting for site terms, rate limits, and privacy obligations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes guidance for anti-bot bypass, CAPTCHA handling, fingerprint spoofing, proxies, and login or session use. <br>
Mitigation: Use it only for websites the user is authorized to access, and check robots.txt, terms of service, rate limits, and privacy rules for each target before running generated crawlers. <br>
Risk: Generated crawlers can collect personal, copyrighted, or otherwise sensitive data, or place load on target services. <br>
Mitigation: Limit collection to necessary data, respect rate limits, avoid republishing restricted content, and review generated scripts before execution. <br>
Risk: Crawler scripts may require cookies, tokens, credentials, proxies, or third-party CAPTCHA services. <br>
Mitigation: Keep secrets out of source code and logs, prefer environment variables or local secret stores, and avoid sharing session material in prompts or generated artifacts. <br>


## Reference(s): <br>
- [ClawHub Web Crawler Skill Page](https://clawhub.ai/moxin1044/web-crawler) <br>
- [Headless Browser Detection Test](https://bot.sannysoft.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python code blocks, shell commands, configuration notes, and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce runnable crawler scripts, dependency installation commands, extraction strategies, export configuration, and compliance reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
