## Description:

Packages skill releases, optionally signs them, and publishes to ClawHub, skillhub.cn, GitHub Releases, or a custom hub hook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to package a skill once, optionally sign it, then publish it to one or more supported registries or create a deterministic package without publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing may expose valuable credentials or files from the publishing environment.

Mitigation: Use an isolated environment with narrowly scoped, short-lived publishing credentials, and inspect the package and destination before publishing.

Risk: Remote unlist and delete capabilities can remove published content beyond ordinary publishing.

Mitigation: Review whether cleanup is needed and confirm the target and release before invoking remote deletion features.

Risk: Security analysis coverage is incomplete because some local references could not be resolved.

Mitigation: Review unresolved references and inspect the skill before installing or running it.

## Reference(s):

- [Clawhub CLI (npm package)](https://www.npmjs.com/package/clawhub)

## Skill Output:

**Output Type(s):** [Files, Shell commands, JSON, Configuration instructions]

**Output Format:** [Release packages (TAR.GZ or ZIP), JSON reports, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Package contents follow configured exclusions and may vary by target.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
