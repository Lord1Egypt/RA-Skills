## Description:

Replace base64 images in session history with context-aware text descriptions, reducing image token cost by 96-99%.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joelovestech](https://clawhub.ai/user/joelovestech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Shrink to reduce image-heavy OpenClaw session history by replacing base64 image blocks with compact, context-aware text descriptions. It is intended for sessions approaching context limits or for teams that need dry-run previews, scoped processing, deduplication, cost estimates, and optional redaction before rewriting session files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session images and nearby conversation context are sent to Anthropic for description generation.

Mitigation: Review the skill before installing in sessions containing secrets, customer data, regulated records, or untrusted screenshots; prefer explicit ANTHROPIC_API_KEY selection and use the narrowest practical session or agent scope.

Risk: The skill permanently rewrites agent history with unvalidated model-generated descriptions.

Mitigation: Run a dry-run first, keep default backups enabled, review output summaries before applying changes, and avoid disabling backups unless another recovery path exists.

Risk: Redaction is performed during model extraction and should not be treated as proof that sensitive source data was never sent externally.

Mitigation: Use --redact when appropriate, but avoid processing sensitive source images unless sending them to the configured Anthropic endpoint is acceptable.

Risk: Broad processing modes can affect many sessions and agents.

Mitigation: Limit scope with --session-file, --agent, --max-images, and --min-tokens; avoid --all-sessions unless the operator has reviewed the expected files and impact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joelovestech/skills/shrink)
- [Publisher profile](https://clawhub.ai/user/joelovestech)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [SECURITY.md](artifact/SECURITY.md)
- [Anthropic Messages API endpoint](https://api.anthropic.com/v1/messages)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown-facing agent guidance with inline shell commands, progress summaries, and optional JSON dry-run or execution results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify OpenClaw session JSONL files by replacing image blocks with text descriptions; creates .bak backups by default unless disabled.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
