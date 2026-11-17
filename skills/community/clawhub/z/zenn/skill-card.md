## Description:

Publish Zenn articles by managing Markdown in a GitHub-connected repository (push/PR -> merge) and previewing with Zenn CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tachi-koma-x](https://clawhub.ai/user/tachi-koma-x)

### License/Terms of Use:


## Use Case:

Developers and content authors use this skill to create, preview, review, and publish Zenn articles or books through a GitHub-connected repository while keeping drafts behind PR review until ready.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accidental disclosure of secrets, customer details, internal URLs, or unreleased metrics through published Zenn content.

Mitigation: Keep drafts unpublished during review, inspect article text and assets before setting published: true, and use the workflow's PR review gate before merging to the publishing branch.

Risk: Installing or updating zenn-cli without version pinning can introduce unreviewed dependency changes.

Mitigation: Pin zenn-cli to a reviewed exact version for normal use and review changelogs before upgrading.

Risk: Direct publishing or incorrect file placement can bypass review or fail to publish expected content.

Mitigation: Use feature branches and PRs, place articles under articles/ and books under books/, and verify local preview output before merge.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and article front matter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow guidance for repository layout, Zenn CLI commands, draft review, and publication checks.]

## Skill Version(s):

0.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
