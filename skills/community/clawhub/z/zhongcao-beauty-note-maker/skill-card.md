## Description:

Creates Xiaohongshu beauty and skincare note packs from supplied product facts, routine context, audience details, and optional paid Xiaohongshu lookup results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agents use this skill to draft Xiaohongshu beauty and skincare post concepts, copy, titles, cover wording, hashtags, and assumptions from user-supplied facts. Optional Xiaohongshu lookup can inform the draft with paid platform reads when the user explicitly approves each lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a shared broad Beatra Device Token with paid-call and local upload capability.

Mitigation: Install only if that authority is acceptable, keep the token out of chat, logs, command arguments, and diffs, and revoke the Beatra authorization when access is no longer needed.

Risk: Optional Xiaohongshu lookups spend credits and can multiply costs if repeated or paged automatically.

Mitigation: Confirm each lookup separately, state the exact credit cost before execution, avoid automatic paging, and treat a skipped lookup as a complete normal run.

Risk: Automatic updates can replace bundled skill code without a separate per-update confirmation.

Mitigation: Use the documented update controls to disable automatic updates when review-before-update is required, and rely on the package's checksum and manifest verification before accepting updates.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/beatra-ai/skills/zhongcao-beauty-note-maker)
- [Beatra Skill Homepage](https://beatra.ai/skills/zhongcao-beauty-note-maker)
- [Beauty note workflow](references/workflow.md)
- [Reading Xiaohongshu](references/note-lookup.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [MCP connection](references/mcp-connection.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown-style note pack with optional inline shell commands and lookup result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typical deliverables include title options, a primary angle, body copy, a four-slide 3:4 plan, cover text, hashtags, a comment starter, assumptions, and any approved lookup cost/result details.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
