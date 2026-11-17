## Description:

Automatically injects relevant skills and protocols into agent context using local embeddings through Ollama with nomic-embed-text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thekhemistai](https://clawhub.ai/user/thekhemistai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this plugin to have agents retrieve and inject relevant local skill and protocol documentation before runs, keeping prompt context focused while preserving custom procedures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote Ollama endpoint receives prompt text and indexed Markdown content, including any secrets or confidential information contained in those docs.

Mitigation: Keep ollamaBaseUrl on localhost, 127.0.0.1, or ::1 unless the remote host is trusted, and do not store secrets in indexed Markdown.

Risk: Server security evidence reports Review-level risk from file path handling.

Mitigation: Use the plugin only in trusted workspaces, restrict configured directories and pinned docs to intended local documentation, and avoid shared or untrusted workspaces until path validation is fixed.

Risk: Server security evidence reports an npm install-name mismatch.

Mitigation: Verify the package name and release version from the ClawHub listing and package metadata before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thekhemistai/skills/skill-preflight)
- [Publisher Profile](https://clawhub.ai/user/thekhemistai)
- [OpenClaw](https://openclaw.ai)
- [Ollama](https://ollama.com)
- [nomic-embed-text](https://ollama.com/library/nomic-embed-text)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown context blocks prepended to agent prompts, with configuration guidance and diagnostic log text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses similarity thresholds, max result limits, pinned documents, line truncation, and per-session deduplication.]

## Skill Version(s):

1.0.5 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
