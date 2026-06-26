## Description: <br>
Python SDK for inference.sh - run AI apps, build agents, and integrate with 150+ models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill for Python integration with inference.sh, including AI app execution, agent development, streaming, file uploads, session management, RAG patterns, and automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is allowed to run local Python commands when invoked. <br>
Mitigation: Review generated commands before execution and run them in an environment where local code execution is acceptable. <br>
Risk: SDK examples use API keys, webhook secrets, file uploads, and persisted chat history. <br>
Mitigation: Protect API keys and webhook secrets, upload only intended files, avoid public uploads for sensitive content, and apply retention controls to chat history. <br>
Risk: The artifact includes unsafe example patterns such as eval() and unvalidated tool execution. <br>
Mitigation: Do not copy those examples into production agents; replace them with validated allowlisted tool handlers and human approval for sensitive actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/okaris/python-sdk) <br>
- [inference.sh](https://inference.sh) <br>
- [Python SDK Reference](https://inference.sh/docs/api/sdk-python) <br>
- [Agent SDK Overview](https://inference.sh/docs/api/agent-sdk) <br>
- [Tool Builder Reference](https://inference.sh/docs/api/agent-tools) <br>
- [Authentication](https://inference.sh/docs/api/authentication) <br>
- [Streaming](https://inference.sh/docs/api/sdk/streaming) <br>
- [File Uploads](https://inference.sh/docs/api/sdk/files) <br>
- [Agent Patterns](references/agent-patterns.md) <br>
- [Tool Builder](references/tool-builder.md) <br>
- [Streaming Reference](references/streaming.md) <br>
- [File Handling](references/files.md) <br>
- [Sessions](references/sessions.md) <br>
- [Async Patterns](references/async-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes synchronous and asynchronous SDK examples, streaming patterns, file upload guidance, session usage, and agent/tool configuration examples.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
