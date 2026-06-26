## Description: <br>
Use xapi CLI to access real-time external data, including Twitter/X profiles, tweets, timelines, crypto token prices and metadata, web search, news, and AI text processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Glacier-Luo](https://clawhub.ai/user/Glacier-Luo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to discover and call xapi CLI capabilities for external data lookups, API proxy calls, OAuth-bound Twitter/X actions, crypto data retrieval, web or news search, and AI text processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize broad external API access, including social posting, OAuth-bound actions, account registration, and payment top-ups. <br>
Mitigation: Require explicit user approval before OAuth binding, POST, DELETE, write, Twitter posting, registration, or top-up actions. <br>
Risk: The xapi API key and payment URLs may expose account authority if logged or shared. <br>
Mitigation: Keep XAPI_API_KEY and local xapi config private, and avoid logging or sharing payment URLs or credentials. <br>
Risk: External processing may expose secrets or sensitive documents to third-party services. <br>
Mitigation: Send sensitive content through xapi only when external processing is acceptable for the user's context. <br>


## Reference(s): <br>
- [xAPI homepage](https://xapi.to) <br>
- [ClawHub skill page](https://clawhub.ai/Glacier-Luo/xapi-labs) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON API responses] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON command inputs or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and an XAPI_API_KEY or xapi account configuration.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
