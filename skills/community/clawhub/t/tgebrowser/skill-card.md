## Description: <br>
Operates TgeBrowser via MCP tools to create or manage environments, groups, proxies, browser automation, and status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuguang2025](https://clawhub.ai/user/tuguang2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage TgeBrowser environments, groups, proxies, profiles, and browser automation through MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent control TgeBrowser profiles through a local MCP/API setup. <br>
Mitigation: Install and enable it only when that level of browser-profile control is intended. <br>
Risk: The skill can retrieve cookies, use logged-in profiles, submit forms, run page scripts, delete profiles, clear cache, and close all profiles. <br>
Mitigation: Require explicit approval before those actions, especially when they affect authenticated sessions or persistent profile data. <br>
Risk: Cookie or proxy credential exposure could leak sensitive account or network access data. <br>
Mitigation: Avoid displaying or sharing raw cookies and proxy credentials unless they are strictly needed for the task. <br>


## Reference(s): <br>
- [TgeBrowser ClawHub skill page](https://clawhub.ai/tuguang2025/tgebrowser) <br>
- [Environment Management](references/environment-management.md) <br>
- [Fingerprint Config](references/fingerprint.md) <br>
- [Proxy Config](references/proxy-config.md) <br>
- [Group Management](references/group.md) <br>
- [System Status](references/system.md) <br>
- [TLS Cipher Values](references/tls-cipher.md) <br>
- [User-Agent Version Values](references/ua-version.md) <br>
- [Country Code Values](references/country-code.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text] <br>
**Output Format:** [Markdown with MCP tool calls, JSON parameters, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser automation actions, profile-management instructions, screenshots, page text, HTML, cookies, user-agent data, or JavaScript evaluation results through TgeBrowser MCP tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
