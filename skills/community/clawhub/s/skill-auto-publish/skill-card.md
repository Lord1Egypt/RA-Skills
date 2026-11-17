## Description:

Safely publish an already-reviewed skill to ClawHub, verify the live registry state, and return a clear release report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[choosenobody](https://clawhub.ai/user/choosenobody)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release operators use this skill to publish already-reviewed ClawHub skills, verify registry and public page state, and return a clear release report with status, issues, and next action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can mutate public ClawHub registry state using user-supplied slug, path, version, and changelog values.

Mitigation: Treat publish inputs as untrusted, validate slug and semver strictly, confirm the source directory and completed release review, and invoke CLI commands with fixed argument arrays or equivalent safe process handling.

Risk: A publish command can succeed while the registry or public page is stale, blocked, or mismatched.

Mitigation: Verify with registry inspection and public page text checks where accessible, and report BLOCKED or MISMATCH instead of PASS when verification cannot be completed.

Risk: Skill source content could accidentally include secrets, private credentials, local-only paths, draft notes, or visible HTML comments.

Mitigation: Run the documented secrets and privacy checklist before publishing and block release when sensitive or unintended content is found.

## Reference(s):

- [Publish Checklist](references/publish-checklist.md)
- [Verification Protocol](references/verification-protocol.md)
- [Local Overrides](references/local-overrides.md)
- [Known Platform Limitations](references/archive/known-platform-limitations.md)
- [Failure Playbook](references/archive/failure-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown release report with status fields, verification results, issues, next action, and inline shell commands when useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include publish status, registry verification, public page verification, skill URL, install command, command used, and follow-up action.]

## Skill Version(s):

2.4.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
