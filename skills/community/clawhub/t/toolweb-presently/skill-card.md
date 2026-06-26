## Description: <br>
AI-powered API for generating structured presentations from text input with customizable themes and formatting options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, content creators, and business automation teams use this skill to call Presently's API and generate structured presentation content from source text with configurable slide count, themes, and colors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation source text and optional email data are sent to ToolWeb's external API. <br>
Mitigation: Avoid confidential, personal, or regulated content unless ToolWeb's privacy and retention terms are acceptable; omit user_email unless needed and use a non-sensitive user_id where possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-presently) <br>
- [Presently API Route](https://api.toolweb.in/tools/presently) <br>
- [Presently API Docs](https://api.toolweb.in:8174/docs) <br>
- [OpenAPI Specification](artifact/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Text] <br>
**Output Format:** [JSON responses containing presentation metadata and generated slide card content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user_id and input_text; optional fields control slide count, format type, theme, colors, and user email.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
