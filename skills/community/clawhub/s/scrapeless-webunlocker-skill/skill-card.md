## Description: <br>
Bypass website blocks and scrape web content using Scrapeless Universal Scraping API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scrapelesshq](https://clawhub.ai/user/scrapelesshq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to fetch, render, and extract content from websites through Scrapeless for authorized scraping, data collection, market intelligence, and automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides broad website bypass and scraping capability with weak target scoping. <br>
Mitigation: Use it only for authorized scraping, define strict target scopes before execution, and review requests that use bypass, proxy, CAPTCHA, or JavaScript rendering options. <br>
Risk: User-supplied URLs, headers, request bodies, proxy settings, and rendering options are sent to a third-party service. <br>
Mitigation: Do not pass cookies, authorization headers, session tokens, private URLs, personal data, or confidential POST bodies unless sharing them with Scrapeless has been approved. <br>
Risk: Non-GET methods and high request volume can increase operational, legal, and billing exposure. <br>
Mitigation: Avoid PUT and DELETE unless explicitly required, monitor Scrapeless rate limits and billing, and reduce request frequency when 429 responses occur. <br>
Risk: Unpinned Python dependencies can change behavior between installs. <br>
Mitigation: Pin and review dependencies before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scrapelesshq/scrapeless-webunlocker-skill) <br>
- [Scrapeless homepage](https://www.scrapeless.com) <br>
- [Scrapeless Universal Scraping API](https://docs.scrapeless.com/en/universal-scraping-api/) <br>
- [Scrapeless Universal Scraping API product page](https://www.scrapeless.com/en/product/universal-scraping-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [JSON containing fetched page content, extracted fields, network logs, or base64 screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X_API_TOKEN and sends target URL, request headers, request body, proxy options, and rendering options to Scrapeless; supports HTML, plaintext, Markdown, PNG, JPEG, network, and content response types.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
