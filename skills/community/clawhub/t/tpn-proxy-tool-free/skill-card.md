## Description: <br>
This skill helps developers generate short-lived SOCKS5 proxy credentials, choose proxy exit regions, check balance, and route basic HTTP requests through distributed proxy nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to create temporary SOCKS5 proxies for multi-region content checks, geo-restricted API testing, crawler IP rotation, and basic proxy-routed HTTP requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proxy-routed requests may expose sensitive traffic to third-party proxy nodes. <br>
Mitigation: Use the skill only for intended proxy testing workflows and avoid sending cookies, tokens, credentials, proprietary data, or other sensitive content through generated proxies. <br>
Risk: The TPN API key and generated proxy username/password are sensitive secrets. <br>
Mitigation: Store the API key in an environment variable, do not hard-code or log secrets, and avoid displaying generated credentials except when needed for the active request. <br>
Risk: Broad proxy activation could route requests through unexpected regions or nodes. <br>
Mitigation: Require explicit user intent, validate destination URLs and proxy parameters, and choose the country, lease duration, and node type deliberately before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/tpn-proxy-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and text or JSON proxy responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include short-lived SOCKS5 proxy credentials, request results, status codes, logs, and balance information.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
