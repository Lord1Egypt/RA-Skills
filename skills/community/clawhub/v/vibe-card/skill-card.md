## Description:

Vibe Card helps an agent generate, manage, share, receive, and synchronize social contact cards and a local contact book.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxd20010606-cmd](https://clawhub.ai/user/sxd20010606-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to create a shareable personal profile card, save received Vibe Card messages, manage contacts, and synchronize contact updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish selected personal profile fields to adonghub.cn.

Mitigation: Confirm the fields that will be published before first use and keep sensitive notes in the local-only fields described by the data format.

Risk: The skill can auto-import contact cards from received Vibe Card messages.

Mitigation: Review cards from untrusted messages before saving or merging them into the contact book.

Risk: The skill can fetch and synchronize contact updates from a remote service.

Mitigation: Keep the server endpoint pinned to the intended HTTPS origin and review sync results before accepting conflict resolutions.

Risk: The skill may ask to create a recurring OpenClaw sync task.

Mitigation: Review the scheduled task command and know how to list or remove the sync job before enabling it.

## Reference(s):

- [Vibe Card Data Format](references/data-format.md)
- [Vibe Card Manual](references/manual.md)
- [ClawHub Skill Page](https://clawhub.ai/sxd20010606-cmd/skills/vibe-card)
- [AdongHub Service](https://www.adonghub.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown and text responses with JSON file updates and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local config.json, profile.json, and contacts.json files; may publish selected profile fields and synchronize contacts with a remote HTTPS service.]

## Skill Version(s):

4.0.0 (source: server release metadata, SKILL.md metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
