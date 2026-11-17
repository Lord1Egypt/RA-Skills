## Description:

Generate, schedule, and publish posts across 10 platforms: X, LinkedIn, Instagram, Threads, Facebook, YouTube, TikTok, Pinterest, Bluesky, and Mastodon, using the user's AI-assisted brand voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmoon90](https://clawhub.ai/user/jmoon90)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and marketing teams use this skill to draft, manage, schedule, and publish social posts through XreplyAI-connected social accounts. It also helps users inspect billing, quota, social account, style, rule, content plan, and posting schedule state before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or schedule public posts and queue recurring automated content generation through connected XreplyAI accounts.

Mitigation: Before publish, schedule, content-plan, or posting-schedule actions, require the agent to show the exact content, account, platform, and time, then wait for explicit user approval.

Risk: The skill can create drafts, upload chosen media files, and change posting preferences or schedules.

Mitigation: Confirm the intended file, preference, schedule, platform, and account before executing changes, and review queue or billing state when quota or plan limits may affect the result.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jmoon90/skills/xreplyai)
- [XreplyAI Homepage](https://xreplyai.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with mcporter shell commands and text or JSON-like tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XREPLY_TOKEN and either mcporter or npx. The skill invokes the @xreplyai/mcp package referenced by the artifact and may depend on connected social accounts, paid-plan features, media file access, quota limits, and schedule constraints.]

## Skill Version(s):

0.3.26 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
