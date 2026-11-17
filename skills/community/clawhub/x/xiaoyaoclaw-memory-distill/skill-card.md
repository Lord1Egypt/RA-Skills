## Description:

Distills OpenClaw conversation history into structured long-term memory and dated daily logs, with deduplication, sensitive-data filtering, and archive-before-overwrite safeguards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtsola](https://clawhub.ai/user/dtsola)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can distill conversation history into a concise long-term MEMORY.md and dated daily logs, with first-run memory building and per-agent organization to keep useful context available across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review coverage was partial: some referenced paths could not be resolved, and the QR image was not analyzed by static analyzers; the clean verdict has medium confidence.

Mitigation: Review the linked source and relevant assets before installation, taking the stated coverage limits into account.

Risk: Saved memory is plaintext and can be read in later sessions.

Mitigation: Review proposed entries before writing, exclude credentials and third-party personal data, and retain the default report-only behavior for scheduled runs unless unattended writes are intentionally enabled.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-memory-distill)
- [Project documentation and source repository](https://github.com/dtsola/xiaoyaoclaw-memory-distill)
- [XiaoyaoClaw](https://www.xiaoyaosai.com/xiaoyaoclaw/)

## Skill Output:

**Output Type(s):** [Markdown, Configuration]

**Output Format:** [Markdown memory files and distillation reports, plus JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-agent workspace files; scheduled runs report only unless autoWrite is explicitly enabled.]

## Skill Version(s):

1.0.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
