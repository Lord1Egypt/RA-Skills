## Description: <br>
Build and route Qwen chat, coding, reasoning, and vision workflows across hosted and self-hosted endpoints with safer debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose, verify, and debug Qwen routes for chat, coding, reasoning, structured output, tool-calling, and vision workflows across hosted Alibaba Cloud Model Studio endpoints and self-hosted OpenAI-compatible servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hosted Qwen routes send prompt content and optional multimodal payloads to Alibaba Cloud Model Studio. <br>
Mitigation: Use hosted endpoints only for data appropriate for that service, or choose a self-hosted Qwen route when data must remain local. <br>
Risk: API keys and local routing notes could expose sensitive configuration if stored incorrectly. <br>
Mitigation: Keep DASHSCOPE_API_KEY in environment variables and store only non-secret routing preferences or sanitized troubleshooting notes in ~/qwen/ after user approval. <br>
Risk: Tool-calling or structured output can drift across model families, backends, chat templates, and parsers. <br>
Mitigation: Validate raw tool responses, use strict schemas and low temperature for automation paths, and fail closed instead of executing guessed arguments. <br>
Risk: Stale model IDs or region mismatches can break production routing. <br>
Mitigation: Verify live model availability through the current surface's /models endpoint before selecting or saving a route. <br>


## Reference(s): <br>
- [Qwen Skill Page](https://clawhub.ai/ivangdavila/qwen) <br>
- [Publisher Profile](https://clawhub.ai/user/ivangdavila) <br>
- [Hosted Qwen Model Discovery - Mainland China](https://dashscope.aliyuncs.com/compatible-mode/v1/models) <br>
- [Hosted Qwen Model Discovery - Singapore](https://dashscope-intl.aliyuncs.com/compatible-mode/v1/models) <br>
- [Hosted Qwen Model Discovery - United States](https://dashscope-us.aliyuncs.com/compatible-mode/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose hosted or self-hosted Qwen routes, endpoint checks, strict JSON validation patterns, troubleshooting steps, and optional local memory notes after user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
