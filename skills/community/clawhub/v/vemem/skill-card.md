## Description:

Visual entity memory that lets an agent remember faces, objects, and places across sessions, resolve images to stable named entities, and attach facts or relationships to those visual identities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linville-charlie](https://clawhub.ai/user/linville-charlie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill when an agent needs persistent visual identity memory: identifying known people or objects in images, labeling new entities, recalling facts about known entities, correcting mistaken identity matches, and handling privacy requests such as forget, restrict, or export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to work with biometric identifiers and persistent local visual-memory stores.

Mitigation: Install in a dedicated virtual environment, set and test VEMEM_HOME, control which images are processed, and confirm consent and deletion requirements before use beyond a personal setup.

Risk: Recalled free-form facts can be inserted into model context and may be incorrect, stale, or adversarial.

Mitigation: Treat recalled facts as untrusted context, not instructions; verify sensitive facts before acting and avoid granting recalled content system-level authority.

Risk: The optional OpenClaw sidecar can automatically process every image attachment once separately enabled.

Mitigation: Use the manual MCP flow by default and enable the sidecar only after confirming the operator accepts always-on image processing.

## Reference(s):

- [vemem homepage](https://github.com/linville-charlie/vemem)
- [MCP tool reference](references/mcp-tools.md)
- [Code recipes](references/examples.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON snippets, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include MCP tool names, local filesystem paths, environment variables, and privacy warnings for biometric data.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
