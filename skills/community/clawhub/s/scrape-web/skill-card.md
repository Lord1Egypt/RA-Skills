## Description: <br>
Uses Python and Scrapling to fetch web page content with support for simple CSS selectors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JnmHub](https://clawhub.ai/user/JnmHub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch web page text, extract CSS selector matches, and optionally save scraped output for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-selected URLs and can write scraped content to a chosen output path. <br>
Mitigation: Run it in a virtual environment, fetch only intended URLs, choose output paths deliberately, and treat scraped webpage text as untrusted. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/JnmHub/scrape-web) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, configuration] <br>
**Output Format:** [Plain text or newline-delimited selector results, with optional file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python with Scrapling and httpx dependencies; network access is expected for user-selected URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
