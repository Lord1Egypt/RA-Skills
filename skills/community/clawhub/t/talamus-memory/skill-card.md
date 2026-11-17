## Description:

Set up and use Talamus as durable, local-first memory for AI agents that need to initialize or diagnose a Talamus brain, ingest files or repositories, retrieve cited context across sessions, inspect note history, verify memory against sources, review proposed corrections, connect Talamus through MCP, or capture a session with explicit consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ampres-ai](https://clawhub.ai/user/ampres-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to configure, operate, and troubleshoot Talamus local memory, including cited retrieval, repository ingestion, verification, MCP setup, and consent-controlled session capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or using Talamus relies on trusting the local package source and CLI behavior.

Mitigation: Install only from a trusted Talamus package source and confirm the installed CLI version before use.

Risk: Session capture can store local memory derived from transcripts and git diffs.

Mitigation: Keep capture disabled unless the user explicitly consents and understands what will be stored.

Risk: Repository scanning, broad brain scopes, and secret overrides can expose sensitive project content.

Mitigation: Preview scans, require explicit approval for broad scopes or --allow-secrets, and avoid exposing secrets from configs, source files, transcripts, or logs.

Risk: LLM-backed memory operations can incur cost or create unsupported recollections.

Mitigation: State planned LLM calls, obtain consent when required, preserve citations, and avoid presenting unsupported memory as verified fact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ampres-ai/skills/talamus-memory)
- [Ampres publisher profile](https://clawhub.ai/user/ampres-ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and occasional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve cited sources, report commands run, and identify any LLM or session-capture activity.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
