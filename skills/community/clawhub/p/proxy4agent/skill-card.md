## Description: <br>
Residential proxy for AI agents to fetch public web content through residential proxy providers with geo-targeting, sticky sessions, search, and browser rendering options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goldentrii](https://clawhub.ai/user/goldentrii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs authorized access to public web pages through a configured proxy provider, including geography-specific requests, repeated requests from a sticky session, search results, or JavaScript-rendered pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Residential proxy access can be misused for blocked sites, CAPTCHA or Cloudflare challenges, login flows, scraping workflows, or other policy-sensitive activity. <br>
Mitigation: Require explicit user approval and a documented authorized, policy-compliant purpose before using the skill for those workflows. <br>
Risk: Proxy providers may see request URLs and response content, including sensitive data if it is sent through the proxy. <br>
Mitigation: Use dedicated provider credentials and avoid sending internal URLs, secrets, private authenticated pages, API keys, or personal data through the proxy. <br>
Risk: Provider usage can create unexpected billing or operational exposure. <br>
Mitigation: Monitor provider usage and billing, and scope credentials to the minimum required provider account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goldentrii/proxy4agent) <br>
- [Project homepage](https://github.com/Goldentrii/proxy4agent) <br>
- [Novada](https://www.novada.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, raw text, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the selected MCP tool and configured proxy provider.] <br>

## Skill Version(s): <br>
1.6.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
