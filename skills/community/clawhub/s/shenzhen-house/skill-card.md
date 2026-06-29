## Description: <br>
小鹿选房 helps agents assist users with Shenzhen housing searches, including second-hand homes, rentals, new homes, price comparison, transaction checks, communities, school districts, and schools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangjike](https://clawhub.ai/user/fangjike) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and real-estate assistants use this skill to search and compare Shenzhen housing options, check communities and school districts, and return concise property guidance with mini-program links. The agent invokes the xiaolu-house CLI, helps with API-key setup when needed, and asks clarifying questions when the user's housing intent is unclear. <br>

### Deployment Geography for Use: <br>
China, primarily Shenzhen <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires running an npm CLI through npx. <br>
Mitigation: Install and run it only when the xiaolu-house package and service are trusted. <br>
Risk: API keys or local configuration may be exposed in ordinary chat or command output. <br>
Mitigation: Use a secure secret-entry flow where available, review config --show output before sharing it, and clear or rotate the API key if exposure is possible. <br>
Risk: The service enforces a one-request-per-second rate limit. <br>
Mitigation: Throttle requests and retry later after 429 responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fangjike/shenzhen-house) <br>
- [xiaolu-house homepage](https://github.com/fanggeek/xiaolu-house) <br>
- [小鹿选房 API key setup](https://www.xiaoluxuanfang.com/claw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise natural-language property summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include mini-program links, CLI help output, configuration guidance, and rate-limit retry guidance.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
