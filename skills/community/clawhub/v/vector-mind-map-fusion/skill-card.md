## Description:

Vector Mind Map Fusion builds, organizes, and queries a layered semantic memory graph from OpenClaw sessions using L1 extraction, L2 consolidation, and L3 vector-plus-keyword recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxiaofeng0811-lgtm](https://clawhub.ai/user/dxiaofeng0811-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to extract useful session content into a structured memory layer, consolidate related memories, and recall prior knowledge through semantic, keyword, and graph-based search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans OpenClaw session history and stores derived memory files.

Mitigation: Install only when persistent local memory is intended, limit access to the generated memory directory, and avoid processing sensitive conversations unless that retention is acceptable.

Risk: Conversation text can be sent to the configured Ollama endpoint for embeddings.

Mitigation: Keep Ollama bound to localhost and do not set OLLAMA_BASE_URL to a remote server unless that data transfer is intended.

Risk: The setup documentation includes curl pipe-to-shell and --break-system-packages installation steps.

Mitigation: Use an isolated virtual environment and review installer commands before execution.

Risk: Optional Feishu notification behavior can involve credentials and recipient identifiers.

Mitigation: Leave Feishu notifications disabled unless the credential and recipient behavior has been reviewed.

Risk: The memory index uses pickle-based HNSW files.

Mitigation: Load index files only from trusted local skill state and avoid sharing or replacing them with untrusted files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxiaofeng0811-lgtm/skills/vector-mind-map-fusion)
- [README](artifact/README.md)
- [L1 extraction flow](artifact/docs/l1_flow.md)
- [L2 consolidation flow](artifact/docs/l2_flow.md)
- [L3 retrieval flow](artifact/docs/l3_flow.md)
- [Recall API](artifact/docs/recall_api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, Python API examples, and text search results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local memory files containing derived session content.]

## Skill Version(s):

1.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
