## Description:

Python SDK for inference.sh - run AI apps, build agents, and integrate with 150+ models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to integrate Python applications with inference.sh, including app execution, streaming, file uploads, stateful sessions, agent workflows, and custom tool definitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calculator and code-execution examples could be copied into an agent in a way that permits unsafe local code execution.

Mitigation: Use safe parsers and explicit approval gates for executable tools instead of copying eval-style examples directly.

Risk: Local file paths, attachments, uploaded files, webhook payloads, and chat history may contain sensitive data that can leave the machine or persist remotely.

Mitigation: Review data before upload, limit public file exposure, protect secrets, and apply retention controls appropriate to the deployment.

Risk: Unpinned package or skill versions can change behavior in controlled environments.

Mitigation: Pin the inferencesh package and the skill release version during production deployment and review updates before rollout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/okaris/skills/python-sdk)
- [inference.sh](https://inference.sh)
- [Python SDK Reference](https://inference.sh/docs/api/sdk-python)
- [Agent SDK Overview](https://inference.sh/docs/api/agent-sdk)
- [Tool Builder Reference](https://inference.sh/docs/api/agent-tools)
- [Authentication](https://inference.sh/docs/api/authentication)
- [Streaming](https://inference.sh/docs/api/sdk/streaming)
- [File Uploads](https://inference.sh/docs/api/sdk/files)
- [Agent Patterns](references/agent-patterns.md)
- [Async Patterns Reference](references/async-patterns.md)
- [File Handling Reference](references/files.md)
- [Sessions Reference](references/sessions.md)
- [Streaming Reference](references/streaming.md)
- [Tool Builder Reference](references/tool-builder.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API usage patterns, package installation commands, environment-variable authentication guidance, and workflow examples.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
