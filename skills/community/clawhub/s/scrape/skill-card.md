## Description: <br>
Legal web scraping with robots.txt compliance, rate limiting, and GDPR/CCPA-aware data handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to plan authorized scraping of public web pages with robots.txt checks, rate limits, and privacy-aware data handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scraping a site without authorization, contrary to robots.txt, terms of service, or available API access may create legal or compliance exposure. <br>
Mitigation: Check robots.txt and site terms before scraping, prefer official APIs, stop when access is disallowed, and use the skill only for authorized public scraping. <br>
Risk: Collected pages may contain personal data or sensitive URL parameters. <br>
Mitigation: Avoid login-protected or personal data, strip unnecessary PII immediately, minimize retained data, and avoid logging sensitive URL parameters. <br>
Risk: Aggressive request behavior can burden target services or trigger rate limits. <br>
Mitigation: Use the documented rate limiting, backoff on 429 responses, identify requests with a contactable User-Agent, and fail closed when compliance checks cannot be completed. <br>


## Reference(s): <br>
- [Scrape on ClawHub](https://clawhub.ai/ivangdavila/scrape) <br>
- [Code patterns](code.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides compliance checklists, scraping boundaries, and reusable request-handling patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
