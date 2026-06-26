## Description: <br>
Ethical web data extraction with robots exclusion protocol adherence, throttled scraping requests, and privacy-compliant handling ("Scrape responsibly!"). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[10OSS](https://clawhub.ai/user/10OSS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Skrape to plan responsible web data extraction, including checking access rules, preferring official APIs, throttling requests, and limiting retention of personal or copyrighted data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sample robots.txt checker can allow scraping when robots.txt cannot be evaluated conclusively. <br>
Mitigation: Review robots.txt and site terms manually, prefer official APIs, and change the checker to fail closed when evaluation is inconclusive. <br>
Risk: Scraping can collect personal data, authenticated content, or sensitive URLs that should not be stored or logged. <br>
Mitigation: Avoid authenticated or personal data unless clearly permitted, limit retention, and redact sensitive URLs from logs. <br>


## Reference(s): <br>
- [Skrape skill instructions](artifact/SKILL.md) <br>
- [Implementation patterns](artifact/code.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code] <br>
**Output Format:** [Markdown with JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance-only release; sample scraping code should be reviewed before use on real sites.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
