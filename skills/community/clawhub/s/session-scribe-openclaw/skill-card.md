## Description: <br>
Automatically summarizes active OpenClaw session transcripts into daily memory files by sending new user and assistant turns to OpenAI or Anthropic for summarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kitsune](https://clawhub.ai/user/kitsune) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to preserve session context as dated Markdown memory notes for later recall or downstream ingestion. It is most useful for unattended or recurring session summarization where explicit transcript and memory paths are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcript content can include secrets, API keys, PII, or other sensitive conversation data that may be sent to OpenAI or Anthropic for summarization. <br>
Mitigation: Run with --dry-run first, avoid sessions containing sensitive data, and use a dedicated low-privilege API key with spend limits. <br>
Risk: Broad unattended use can summarize more sessions than intended and store reusable memory notes from those sessions. <br>
Mitigation: Start with one explicit session before using --all-sessions, set --active-within-hours appropriately, and remove the cron job when unattended summarization is no longer wanted. <br>
Risk: API key handling can expose credentials if keys are placed directly in shell history or cron entries. <br>
Mitigation: Store keys in a protected file, use --api-key-file, restrict file permissions, and pass --provider when needed to avoid provider auto-detection mistakes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kitsune/session-scribe-openclaw) <br>
- [OpenClaw Transcript Format](references/transcript-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown memory files with timestamped bullet-point summaries and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and an OpenAI or Anthropic API key; supports dry-run mode, explicit session selection, and all-sessions cron operation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
