## Description: <br>
Structured knowledge extraction MCP server for ClawHub/OpenClaw that converts remote media URLs into summaries, topics, action items, Q&A, flashcards, entities, confidence scores, and workflow traces through one task-oriented tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuyuew1991](https://clawhub.ai/user/shuyuew1991) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this MCP server to convert remote audio or video into structured knowledge artifacts for downstream products, search, education, meeting workflows, and content generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media URLs, transcript text, chunk context, and optional knowledge-model prompts may be sent to configured external transcription and model services. <br>
Mitigation: Audit and trust the configured endpoints before deployment, prefer HTTPS for non-local services, and document the data flow for users. <br>
Risk: The server requires a sensitive videomp3word session cookie and can optionally use API keys for upstream and model services. <br>
Mitigation: Use a dedicated upstream account, inject credentials only at runtime, and avoid committing secrets into packages or environment files. <br>
Risk: Publicly exposed HTTP or MCP endpoints may process requests without the intended access controls if bearer keys are not configured. <br>
Mitigation: Set MCP_ACCESS_KEYS, use NODE_ENV=production for exposed deployments, and prefer localhost or authenticated infrastructure. <br>
Risk: Persistent MongoDB storage can retain media, transcript, workflow, and knowledge records beyond the immediate session. <br>
Mitigation: Define retention controls before enabling MongoDB and align storage behavior with the deployment's data handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuyuew1991/videomp3word-mcp) <br>
- [README](README.md) <br>
- [Sample output](examples/sample_output.json) <br>
- [videomp3word service](https://videomp3word.com) <br>
- [DashScope-compatible API endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Structured JSON responses with optional Markdown and Notion-ready exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include summary, topics, key points, action items, Q&A pairs, flashcards, entities, confidence scores, exports, and workflow trace data.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
