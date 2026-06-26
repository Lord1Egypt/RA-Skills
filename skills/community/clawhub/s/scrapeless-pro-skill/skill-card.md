## Description: <br>
Professional web scraping for OpenClaw using stealth Playwright automation, anti-bot bypass, JavaScript rendering, and structured data extraction from modern websites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[showmemercy19-rgb](https://clawhub.ai/user/showmemercy19-rgb) <br>

### License/Terms of Use: <br>
Commercial <br>


## Use Case: <br>
Developers and external OpenClaw users use Scrapeless Pro to scrape authorized web pages, render JavaScript-heavy sites, and extract structured data through a CLI or programmatic API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stealth scraping can be used against sites where the user lacks permission or where scraping is prohibited. <br>
Mitigation: Restrict use to sites the user owns or has permission to scrape, and avoid sensitive or authenticated pages. <br>
Risk: The validate command prints the full license key to logs. <br>
Mitigation: Do not run the validate command until license-key logging is fixed, or only run it where stdout is not captured or retained. <br>
Risk: Browser automation can collect more page data than intended. <br>
Mitigation: Use explicit selectors and review output before storing, sharing, or acting on scraped data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/showmemercy19-rgb/scrapeless-pro-skill) <br>
- [Scrapeless Pro Homepage](https://cosmic-lollipop-a61cc5.netlify.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [JSON, CSV, Markdown, or saved files containing scraped page data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npx, Playwright, and SCRAPELESS_LICENSE_KEY.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
