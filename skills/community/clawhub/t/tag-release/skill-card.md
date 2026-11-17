## Description:

Creates and pushes date-based release tags, and matching GitHub releases, for one or more configured microservice repositories from a selected branch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunyang777](https://clawhub.ai/user/sunyang777)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to prepare release tag operations for configured services, choose the target branch or explicit tag name, run dry runs when needed, and report tag, release, and pull request details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports plaintext service credentials in the package.

Mitigation: Do not install or run the package as-is; rotate exposed credentials and replace bundled secrets with placeholders or runtime secret loading before use.

Risk: The release evidence reports broad write behavior for multi-repository tag and release creation.

Mitigation: Require explicit service selection or a separate confirmed bulk flag before any non-dry-run operation.

Risk: The skill performs real remote GitHub tag and release writes.

Mitigation: Use dry-run mode first and review the selected services, branch, tag name, and target commits before allowing writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunyang777/skills/tag-release)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with shell command invocations and release operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include processed service names, target branch, tag name, dry-run status, tag and release links, latest pull request details, and failure reasons.]

## Skill Version(s):

1.0.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
