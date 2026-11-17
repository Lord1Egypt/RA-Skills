## Description:

Turns NxVET voice notes and button recordings into local reminders, iCalendar event files, and a daily triage note without sending calendar or message actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[talnirnx](https://clawhub.ai/user/talnirnx)

### License/Terms of Use:

MIT-0

## Use Case:

External clinic operators and their agents use this skill to build a local poller that turns NxVET recordings into reviewable reminders, triage notes, and .ics calendar files while keeping downstream outputs on the operator's machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinic-sensitive transcripts may be visible to the active agent during classification.

Mitigation: Use only when authorized to process the clinic's recordings, and classify transcripts in a constrained mode that treats transcript text as untrusted data.

Risk: The NxVET organization API key can expose sensitive organization data if leaked or over-scoped.

Mitigation: Prefer the bundled REST poller, use a narrowly scoped read-only key if available, store the key only in .env, and never paste, print, or commit the full key.

Risk: Local state, transcripts, and generated reminder outputs can contain patient or clinic-sensitive content.

Mitigation: Keep .env, state, and output directories out of git and sync folders unless the operator explicitly approves the storage location.

Risk: Generated reminders or calendar files may reflect ambiguous transcript interpretation.

Mitigation: Quote the original transcript in outputs, put unclear items in an Unclear bucket, and require the operator to review .ics files before importing them.

## Reference(s):

- [NxVET Voice Notes Skill Homepage](https://api.nx.vet/skills.html#voice-notes)
- [NxVET API Documentation](https://api.nx.vet/)
- [NxVET Agent API Guide](https://api.nx.vet/llms-full.txt)
- [NxVET OpenAPI Specification](https://api.nx.vet/openapi/nxvet-api.yaml)
- [NxVET MCP Setup](https://api.nx.vet/mcp.html)
- [Security and Privacy](reference/security.md)
- [Caching, State, and Idempotency](reference/caching-and-state.md)
- [Good Practices](reference/good-practices.md)
- [NxVET API Reference Notes](reference/nxvet-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with Python scripts and generated local Markdown, JSON, and iCalendar files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and NXVET_API_KEY; generated runtime state and output files should remain local and git-ignored.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
