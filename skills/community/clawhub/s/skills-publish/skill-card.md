## Description:

Publish an OpenClaw skill to ClawHub with release checks, version metadata, and command generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fwwdn](https://clawhub.ai/user/fwwdn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit a local OpenClaw skill package, collect release metadata, and generate a reviewed ClawHub publish command before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated publish command could target the wrong skill folder, slug, version, changelog, tags, or display name.

Mitigation: Review every generated command argument and release metadata field before approving any publish action.

Risk: Local readiness checks cannot prove ClawHub authentication state or confirm that the live listing updated correctly.

Mitigation: Confirm the active account with clawhub whoami before publishing and verify the published skill page or search result afterward.

Risk: The helper checks packaging and release inputs, but does not independently establish skill quality, discoverability, or runtime behavior.

Mitigation: Use additional review such as skill testing, listing review, or comparison with the currently published version when release confidence is low.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/fwwdn/skills/skills-publish)
- [ClawHub Publisher Profile](https://clawhub.ai/user/fwwdn)
- [Publish Flow](artifact/references/publish-flow.md)
- [Release Checklist](artifact/references/release-checklist.md)
- [Local Release Checklist](artifact/references/checklist.md)
- [Common Errors](artifact/references/common-errors.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and release-check findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a generated clawhub publish command after slug, display name, version, changelog, and tags are reviewed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
