## Description:

X Social Manager Dist helps an agent craft, review, optimize, and schedule X/Twitter posts, threads, replies, DMs, and growth strategy with account research and local strategy memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rabden](https://clawhub.ai/user/rabden)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, developers, founders, and professionals use this skill to build and operate an X/Twitter content workflow, including onboarding, profile analysis, post and reply drafting, content planning, engagement review, and DM outreach. The skill can prepare public posting commands but requires explicit user approval before posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate with an authenticated X account and prepare public posts, replies, likes, reposts, follows, or DMs.

Mitigation: Require explicit approval before any public action, review all generated text and commands, and restrict activation to intended social-media tasks.

Risk: The setup flow can install command-line tools and includes an automatic curl-to-shell installation path.

Mitigation: Review or remove the automatic install path, install dependencies manually when possible, and pin or verify tool sources before use.

Risk: The skill stores identity, voice, audience, reply history, leads, and performance notes in local plaintext markdown files.

Mitigation: Inspect the generated files regularly, avoid storing unnecessary sensitive data, and delete or redact local memory and strategy files when no longer needed.

Risk: Generated social strategy or engagement advice could be inaccurate, outdated, or misaligned with the user's brand.

Mitigation: Treat drafts and analysis as proposals, verify claims before posting, and update the profile, memory, and strategy files with corrected preferences and outcomes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rabden/skills/x-social-manager-dist)
- [README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)
- [Twitter CLI Reference](artifact/references/cli-reference.md)
- [Content Strategy Reference](artifact/references/content-strategy.md)
- [Hook Library](artifact/references/hook-library.md)
- [X Algorithm Playbook](artifact/references/algorithm-playbook.md)
- [Voice Anti-Patterns](artifact/references/voice-anti-patterns.md)
- [Memory Log](artifact/references/memory.md)
- [User Profile](artifact/references/user-profile.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline shell commands, structured post and reply drafts, character counts, approval prompts, and strategy-file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local profile, memory, planning, and strategy files and may propose twitter-cli commands for approved actions.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
