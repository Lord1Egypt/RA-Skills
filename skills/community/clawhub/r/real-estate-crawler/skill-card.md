## Description: <br>
Crawls major Chinese real estate listing sites such as Anjuke, Beike, Lianjia, and Soufun, with property data extraction and documented anti-crawling workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h8296699](https://clawhub.ai/user/h8296699) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill to collect property listing data from Chinese real estate platforms for market research, comparison, and analysis where they have explicit authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes anti-bot, CAPTCHA, proxy, cookie, and session-reuse workflows that may create legal, platform-policy, privacy, account, or session risks. <br>
Mitigation: Install and use only with explicit authorization for the target sites; prefer official APIs or licensed datasets, and avoid CAPTCHA-solving services, proxy rotation for evasion, and reuse of verified browser sessions. <br>
Risk: Saved cookies, browser sessions, screenshots, or page dumps may contain sensitive account or browsing data. <br>
Mitigation: Delete saved cookies, sessions, screenshots, and page dumps promptly, and avoid storing reusable authenticated session material. <br>
Risk: Website structure changes, CAPTCHA challenges, or anti-crawling updates can make extracted property data incomplete or inaccurate. <br>
Mitigation: Validate extracted records against the live site, review selectors before relying on results, and treat crawler output as unverified data until checked. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/h8296699/real-estate-crawler) <br>
- [README](artifact/README.md) <br>
- [Anti-crawler guide](artifact/docs/anti_crawler_guide.md) <br>
- [Captcha strategies](artifact/docs/captcha_strategies.md) <br>
- [Publish notes](artifact/publish.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands, Python code references, and generated JSON, CSV, or HTML data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and agent-browser; outputs depend on target site availability, authorization, and selected crawl mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
