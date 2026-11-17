## Description:

Operate assigned GitLab work with owner-verified project access and guarded MR delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xrowgmbh](https://clawhub.ai/user/xrowgmbh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to manage GitLab work items and merge requests, move assigned work through review, and report queue progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious. Scanner evidence reports that it can claim unassigned work and make GitLab changes, including label changes after project access checks fail; scan coverage is incomplete.

Mitigation: Install only if you trust these actions and their scope. Review the skill and use a narrowly scoped GitLab token, then monitor its changes.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/xrowgmbh/skills/xrowgmbh-gitlab-agent)
- [GitLab Agent Skill source](https://gitlab.com/xrow-public/helm-openclaw/-/tree/main/profile/eugene-harold-krabs/skills/gitlab-agent)
- [GitLab default roles](https://docs.gitlab.com/user/permissions/#default-roles)
- [GitLab contribution guide](https://docs.gitlab.com/development/contributing/#make-changes-and-open-a-merge-request)
- [OpenClaw skill authoring guide](https://docs.openclaw.ai/tools/creating-skills)
- [Discovery performance notes](artifact/references/discovery-performance.md)
- [Documentation style guide](artifact/references/documentation-style.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Markdown, GitLab work item and merge request changes]

**Output Format:** [GitLab updates, code changes, and Markdown work summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make remote GitLab changes using the configured account.]

## Skill Version(s):

1.147.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
