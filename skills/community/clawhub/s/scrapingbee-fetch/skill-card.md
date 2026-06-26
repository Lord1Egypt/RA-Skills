## Description: <br>
Advanced JavaScript web page renderer using ScrapingBee API. Extracts main content and returns clean Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flobo3](https://clawhub.ai/user/flobo3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch JavaScript-heavy web pages through ScrapingBee and return the extracted page title and relevant body text as clean Markdown for analysis or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs are sent to ScrapingBee as a third-party processor. <br>
Mitigation: Use only for URLs whose data flow is approved, and avoid private, internal, token-bearing, or sensitive research URLs unless that processing is authorized. <br>
Risk: The skill depends on a ScrapingBee API key. <br>
Mitigation: Keep SCRAPINGBEE_API_KEY out of source control and provide it through the runtime environment or an approved secrets mechanism. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flobo3/scrapingbee-fetch) <br>
- [ScrapingBee](https://www.scrapingbee.com/) <br>
- [ScrapingBee dashboard](https://dashboard.scrapingbee.com/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCRAPINGBEE_API_KEY and sends requested URLs to ScrapingBee for fetching and rendering.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
