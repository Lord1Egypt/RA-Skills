## Description:

Prove user-visible OpenClaw Telegram behavior on Telegram's Test Server with Convex-leased team credentials; drive real-user turns and record messages, edits, deletions, reactions, typing, or rich content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to exercise OpenClaw Telegram behavior as a dedicated Test Server user and preserve evidence of what the user sees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags a medium-confidence, incomplete-evidence concern about a mock-based test path in a skill described as testing real-user behavior; this is a review decision, not a claim of malicious intent.

Mitigation: Before installing, consider whether the mock-based workflow fits your needs and verify the stated live-server testing and credential handling.

Risk: The workflow uses leased test credentials and records Telegram activity.

Mitigation: Keep credentials, identities, and private paths out of shared logs and reports, and complete the documented lease and process cleanup.

## Reference(s):

- [ClawHub release](https://clawhub.ai/hillstreet-ph/skills/telegram-e2e-userbot)
- [Telegram E2E verification map](features/README.md)
- [Runtime reference](features/runtime-reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON, NDJSON]

**Output Format:** [Markdown guidance and shell commands; JSON summaries and NDJSON event recordings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proof artifacts record observed Telegram events and test outcomes; keep credentials, identities, and private paths out of shared reports.]

## Skill Version(s):

1.0.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
