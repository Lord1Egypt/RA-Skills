## Description:

Organizes PC WeChat attachments on Windows, macOS, and Linux by type, customer, or custom rules, previews the plan, then copies selected files to a chosen folder; it can also prepare an optional knowledge-base import manifest and does not access or decrypt chat databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samjoeyang](https://clawhub.ai/user/samjoeyang)

### License/Terms of Use:

MIT-0

## Use Case:

PC WeChat users use this skill to find, classify, deduplicate, and copy local chat attachments into an organized folder. They can optionally prepare selected files for import into a knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe rules or file lists can redirect writes outside the chosen folder or overwrite files.

Mitigation: Prefer a version with destination containment and overwrite protection; otherwise restrict execution to a sandbox with only intended files accessible, inspect rules and manifests, and back up existing outputs.

Risk: An approved knowledge-base upload could target the wrong account or space.

Mitigation: Select the intended accounts and explicitly approve each upload and destination space.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/samjoeyang/skills/wechat-attachment-organizer)

## Skill Output:

**Output Type(s):** [Files, JSON, Guidance]

**Output Format:** [JSON manifests and reports, an organized copy of selected attachments, and a preview plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview by default; copying requires explicit confirmation and --apply.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
