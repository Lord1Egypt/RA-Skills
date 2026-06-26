## Description: <br>
Automatically enables a local SOCKS5/HTTP proxy for selected external sites and APIs, including GitHub, OpenAI, npm, and PyPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tedtalk](https://clawhub.ai/user/Tedtalk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run network commands through a local proxy when accessing approved external services, package registries, and APIs. It is most relevant in environments where direct outbound access is unavailable or unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network requests, destinations, package downloads, credentials, or payloads may transit an insufficiently described third-party proxy path. <br>
Mitigation: Install and use only when the proxy operator is trusted, route only explicitly approved traffic through it, avoid sending secrets unless necessary, and disable the proxy when it is not needed. <br>


## Reference(s): <br>
- [Proxy Auto ClawHub release](https://clawhub.ai/Tedtalk/proxy-auto) <br>
- [Tedtalk publisher profile](https://clawhub.ai/user/Tedtalk) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May export proxy-related environment variables before executing the requested command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
