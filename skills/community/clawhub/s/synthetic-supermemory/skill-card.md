## Description: <br>
Synthetic Supermemory automates persistent memory for OpenClaw agents by summarizing session transcripts into daily memory files, ingesting them into Supermemory, and retrieving relevant context at session startup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kitsune](https://clawhub.ai/user/kitsune) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent, cross-session memory to OpenClaw agents. It can scribe active conversations, store structured memory in local markdown and Supermemory containers, and recall relevant context for later sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated memory collection can process private OpenClaw transcripts and send derived content to external services. <br>
Mitigation: Install only when persistent memory is intended, start with dry runs, review or redact memory files before upload, and use dedicated low-privilege API keys with spend limits. <br>
Risk: Broad all-session cron usage can repeatedly capture more conversation history than intended. <br>
Mitigation: Begin with explicit sessions or narrow containers, set the provider explicitly, avoid broad all-session cron until trusted, and keep a clear removal path for cron entries and keys. <br>
Risk: Persistent memory may retain sensitive, stale, or incorrect information after it has been written. <br>
Mitigation: Review stored memory files and use Supermemory container scoping, delete, and forget operations when memories should be corrected or removed. <br>


## Reference(s): <br>
- [Supermemory API Reference](references/api.md) <br>
- [OpenClaw Transcript Format](references/transcript-format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kitsune/synthetic-supermemory) <br>
- [Supermemory API](https://api.supermemory.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown memory files, CLI text output, setup command snippets, and Supermemory API writes or searches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses per-agent container tags; requires node, SUPERMEMORY_API_KEY, and an OpenAI or Anthropic API key for transcript summarization.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
