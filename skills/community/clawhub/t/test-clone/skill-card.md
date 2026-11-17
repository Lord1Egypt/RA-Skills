## Description:

Use the ClawHub CLI to search, install, update, and publish agent skills from clawhub.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krischristen-hash](https://clawhub.ai/user/krischristen-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage ClawHub skills from the command line, including search, install, update, listing, authentication, and publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned global CLI install can pull a version that has not been reviewed for this environment.

Mitigation: Install the CLI from a trusted registry and prefer a pinned, reviewed package version.

Risk: Bulk forced noninteractive updates can change multiple installed agent skills with little user review.

Mitigation: Prefer updating a single named skill first; use bulk forced updates only when the operator intentionally wants multiple installed skills changed.

Risk: Publishing a broad target directory can unintentionally include secrets or unrelated local files.

Mitigation: Review the target directory before publishing and publish only the intended named skill folder.

## Reference(s):

- [Test Clone Skill Page](https://clawhub.ai/krischristen-hash/skills/test-clone)
- [ClawHub Registry](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the clawhub CLI binary; examples include npm installation, registry/workdir configuration, authentication, search, install, update, list, and publish commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
