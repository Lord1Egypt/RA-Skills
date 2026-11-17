## Description:

Skill Factory helps OpenClaw agents turn ideas or source material into structured, versioned, publishable skills and upgrade existing skills through a repeatable workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhelunsun](https://clawhub.ai/user/zhelunsun)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill authors use Skill Factory to capture requirements, collect source material, draft skill files, manage versions, and prepare releases for GitHub or ClawHub. It is intended for creating new OpenClaw skills and maintaining existing ones through structured upgrade plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to create and modify skill repositories, which can introduce incorrect instructions or unwanted file changes.

Mitigation: Require an explicit plan, review exact target paths and proposed files, and inspect diffs before applying or publishing changes.

Risk: Publishing and upgrade workflows can expose unintended content if repository remotes, visibility, changelog text, or generated files are not reviewed.

Mitigation: Verify Git remotes and visibility, scan for secrets, confirm the publish command and changelog, and pin the ClawHub CLI version before release.

Risk: Recurring sync automation can alter the active workspace without enough final review.

Mitigation: Avoid enabling recurring sync automation unless the workspace is fully controlled and approvals are required for release-impacting changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhelunsun/skills/skillfactory)
- [README](README.md)
- [Skill SOP](SKILL-SOP.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and generated repository files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update skill files, changelog entries, release plans, and publish or sync commands when the user approves those workflows.]

## Skill Version(s):

2.4.0 (source: frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
