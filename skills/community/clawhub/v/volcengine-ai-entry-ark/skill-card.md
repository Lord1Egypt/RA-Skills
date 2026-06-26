## Description: <br>
Entry skill for Volcengine ARK model invocation and routing, including request templates, endpoint setup, model routing, and authentication troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to start Volcengine ARK chat/completion calls, collect required endpoint and generation settings, and troubleshoot common API errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ARK API keys could be exposed or over-scoped when used in generated request examples. <br>
Mitigation: Use a scoped ARK API key and redact Authorization headers from logs, shared traces, and support material. <br>
Risk: Requests may be sent to the wrong ARK endpoint or region. <br>
Mitigation: Confirm the endpoint ID, region, and domain before sending requests. <br>
Risk: Sensitive prompts or data may be sent to Volcengine ARK without appropriate approval. <br>
Mitigation: Avoid sending sensitive prompts unless the user's Volcengine data-handling requirements allow it. <br>


## Reference(s): <br>
- [Volcengine ARK chat completions endpoint](https://ark.cn-beijing.volces.com/api/v3/chat/completions) <br>
- [Skill source references](references/sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/volcengine-ai-entry-ark) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance, Troubleshooting guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the user's ARK API key, endpoint ID, task type, and optional generation parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
