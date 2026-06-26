## Description: <br>
Fetches webpage content with a stealth-enabled headless browser and converts the captured HTML into readable Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlutwuwei](https://clawhub.ai/user/dlutwuwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve authorized webpages, including news, finance pages, and long-form pages, and receive the page title plus Markdown content for downstream reading or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses stealth browser automation against arbitrary URLs and disables Chromium sandboxing. <br>
Mitigation: Use it only for authorized sites, avoid secrets or internal addresses in URLs, and run it in an isolated environment. <br>
Risk: The skill is designed to bypass basic anti-crawling checks. <br>
Mitigation: Confirm that automated access is permitted for the target site before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlutwuwei/web-anti-crawl-fetch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Console text with progress messages, page title, and Markdown body content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown output is truncated to 20,000 characters by the script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
