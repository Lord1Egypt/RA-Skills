## Description: <br>
Legal web scraping with robots.txt compliance, rate limiting, and GDPR/CCPA-aware data handling. Supports both direct HTTP scraping and managed scraping via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data teams use this skill to plan and implement legal web scraping workflows for public pages, including robots.txt checks, rate limiting, PII minimization, direct HTTP scraping, and managed scraping through SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Managed scraping uses a sensitive SkillBoss API key and can send scraped content to a third-party service. <br>
Mitigation: Keep SKILLBOSS_API_KEY in a local secret store or environment variable, and do not send private pages, login-protected content, personal data, or sensitive business data into managed scraping or LLM examples. <br>
Risk: Scraping without authorization can create legal, terms-of-service, privacy, or server-load risk. <br>
Mitigation: Scrape only public pages you are authorized to access, verify robots.txt and site terms, use an official API when one is available, rate limit requests, respect 429 responses, and minimize or strip PII unless legally justified. <br>


## Reference(s): <br>
- [Scrape code patterns](code.md) <br>
- [ClawHub release page](https://clawhub.ai/tobeyrebecca/toby-scrape) <br>
- [SkillBoss API Hub pilot endpoint](https://api.skillbossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, API calls, configuration] <br>
**Output Format:** [Markdown guidance with Python code examples and API call patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Managed scraping examples require SKILLBOSS_API_KEY; direct HTTP examples do not require managed-service credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
