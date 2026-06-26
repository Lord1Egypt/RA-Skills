## Description: <br>
Zyla API Hub Skill turns an OpenClaw AI agent into a real-world operator with access to 10,000+ production-ready APIs from Zyla API Hub, including weather, finance, translation, email validation, geolocation, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alebrega](https://clawhub.ai/user/alebrega) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent discover and call Zyla API Hub services for tasks such as weather lookup, currency conversion, email validation, geolocation, and other API-backed workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize broad, billable calls to Zyla APIs and may send user request data to Zyla or downstream API providers. <br>
Mitigation: Use a dedicated API key, monitor billing and usage, avoid sensitive inputs unless needed, and require explicit approval before paid or mutating API calls. <br>
Risk: The skill handles a Zyla API key for authenticated calls. <br>
Mitigation: Configure the key through OpenClaw configuration or environment variables, do not paste it into chat, and avoid logging or sharing the raw key. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alebrega/zyla-api-hub-skill) <br>
- [Zyla OpenClaw Connect](https://zylalabs.com/openclaw/connect) <br>
- [Zyla API Hub](https://zylalabs.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Zyla API response data, rate-limit metadata, setup steps, and API-key configuration guidance.] <br>

## Skill Version(s): <br>
1.0.7 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
