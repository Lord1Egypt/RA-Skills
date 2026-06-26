## Description: <br>
Extract structured data from websites using Zyte API with smart proxy rotation and browser rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw to Zyte API through ClawLink, discover available Zyte tools, extract structured data from URLs, check service health, and review account usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Zyte API account and ClawLink plugin access, so requests may use account-scoped credentials and consume paid quota. <br>
Mitigation: Install only when the user is comfortable connecting Zyte API through ClawLink, verify the active connection before calls, and apply extra scrutiny to high-volume or cost-sensitive scraping. <br>
Risk: URLs, request parameters, and extracted page content may be processed by ClawLink and Zyte. <br>
Mitigation: Avoid secrets-bearing links, internal systems, private pages, regulated data, and scraping that lacks authorization or violates applicable terms. <br>
Risk: Broad or repeated extraction can create privacy, cost, authorization, or terms-of-service issues. <br>
Mitigation: Prefer targeted extraction, require explicit confirmation for high-volume or repeated scraping, respect robots.txt and website terms, and report real tool errors without inventing results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/zyte-api-scraping) <br>
- [Zyte API Documentation](https://docs.zyte.com/zyte-api/) <br>
- [Zyte API Overview](https://www.zyte.com/zyte-api/) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zyte-api-scraping) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ClawLink tool calls that return structured data, service status, incidents, maintenance windows, account details, or usage information.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
