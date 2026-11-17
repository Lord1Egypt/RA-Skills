## Description:

Synthetic Supermemory helps OpenClaw agents summarize session transcripts into structured memory files, ingest those memories into Supermemory, and retrieve relevant context at session startup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kitsune](https://clawhub.ai/user/kitsune)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent operators use this skill to create persistent cross-session memory without relying on agents to manually report what should be remembered. It is suited for workflows that need automated session summarization, semantic memory search, and startup context recall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent OpenClaw session content and selected memory files may be processed by external LLM providers and stored in Supermemory.

Mitigation: Use dedicated low-privilege API keys with spending limits, redact sensitive content before ingestion, and limit the agents and memory directories passed to the scripts.

Risk: Automated cron jobs can continue processing session content after the operator no longer intends to maintain automated memory.

Mitigation: Run dry-run first, install cron entries only for intended scopes, and remove the cron entries when automated processing is no longer wanted.

Risk: Credential handling needs review when multiple LLM provider keys are present.

Mitigation: Avoid setting both LLM provider keys until the provider/key issue identified in the security guidance is fixed, and store secrets in restricted key files rather than directly in crontab.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kitsune/skills/synthetic-supermemory)
- [Supermemory API Reference](references/api.md)
- [OpenClaw Transcript Format](references/transcript-format.md)
- [Supermemory API](https://api.supermemory.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, plus CLI text output and generated markdown memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, SUPERMEMORY_API_KEY, and an OpenAI or Anthropic API key for transcript summarization.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
