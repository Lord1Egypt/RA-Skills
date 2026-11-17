## Description:

Helps an agent search, transfer, share, organize, and summarize files in a user's Quark Drive account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quarkdrive](https://clawhub.ai/user/quarkdrive)

### License/Terms of Use:

MIT-0

## Use Case:

Quark Drive users can authorize an agent to find, upload, download, share, rename, organize, and summarize their cloud files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can download and execute unverified remote code or update the local runtime.

Mitigation: Install only from a trusted publisher and review installation and update actions before running them.

Risk: CLI calls forward raw user prompts, which may contain sensitive information.

Mitigation: Avoid sensitive prompts unless forwarding their complete text is acceptable.

Risk: Account operations and uninstall actions can change authorization, local tooling, or cloud-file organization.

Mitigation: Review requested changes and uninstall actions, and confirm file scope before bulk operations.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/quarkdrive/skills/quarkclouddrive)
- [ClawHub publisher](https://clawhub.ai/user/quarkdrive)
- [Quark Drive](https://pan.quark.cn)
- [Authorization guide](references/auth.md)
- [File operations guide](references/file-ops.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Text and Markdown with CLI commands and cloud-file results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file links, summaries, and operation results; account operations require authorization.]

## Skill Version(s):

1.0.23 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
