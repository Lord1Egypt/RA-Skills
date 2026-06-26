## Description: <br>
Provides guidance for using UAPI's GET /ai/translate/languages endpoint to retrieve AI translation language and configuration options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to identify when the UAPI AI translation language configuration endpoint is appropriate, then confirm its request path, authentication considerations, and response code before calling it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Implicit invocation may cause an agent to contact uapis.cn for matching translation configuration requests. <br>
Mitigation: Enable the skill only for workflows that need UAPI translation language configuration and review network access expectations before deployment. <br>
Risk: Using a UAPI Key shares credentials with the UAPI service. <br>
Mitigation: Provide a UAPI Key only when the task needs stable quota-backed access and the service is trusted for that workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuakami/uapi-get-ai-translate-languages) <br>
- [Quick start](references/quick-start.md) <br>
- [AI translation configuration operation](references/operations/get-ai-translate-languages.md) <br>
- [Translate resource overview](references/resources/Translate.md) <br>
- [UAPI service](https://uapis.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls] <br>
**Output Format:** [Markdown or text guidance for preparing a GET request and interpreting endpoint documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The endpoint has no explicit parameters; stable use may require a UAPI Key when anonymous quota or rate limits are reached.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
