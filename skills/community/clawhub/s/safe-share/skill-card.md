## Description:

Safe Share sanitizes logs, configs, prompts, stack traces, and skill content before public sharing by replacing API keys, tokens, cookies, passwords, emails, IPs, and other sensitive values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nighty35628](https://clawhub.ai/user/nighty35628)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and external users use Safe Share to create a safe-to-share copy of logs, configs, prompts, stack traces, and skill content before posting publicly. It helps reduce accidental disclosure of credentials and sensitive identifiers while preserving enough surrounding structure for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deterministic sanitization can miss custom identifiers, names, addresses, or context-specific sensitive data.

Mitigation: Use the skill as a local first pass and manually review the sanitized output before public sharing.

Risk: A broad scan could expose or alter unrelated content outside the intended sharing workflow.

Mitigation: Run the sanitizer only on the exact text or file the user asks to make shareable.

Risk: Summaries that include raw matched values could re-disclose the sensitive content being sanitized.

Mitigation: Report only finding types and counts, and keep review notes high level.

## Reference(s):

- [Safe Share ClawHub Page](https://clawhub.ai/nighty35628/skills/safe-share)
- [Detection Patterns](references/patterns.md)
- [Output Format](references/output-format.md)
- [Representative Test Cases](references/test-cases.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [JSON or human-readable Markdown with sanitized text, findings summary, and review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not include raw matched sensitive values; supports placeholder, redact, and mask replacement modes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
