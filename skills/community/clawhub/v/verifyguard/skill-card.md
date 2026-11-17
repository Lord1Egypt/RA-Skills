## Description:

VerifyGuard prechecks AI-generated Markdown before publishing or submission for completeness, link syntax, sensitive information, and formatting issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxr-666](https://clawhub.ai/user/lxr-666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agents use this skill to inspect Markdown content before publication or task submission. It reports potential completeness, formatting, link, and sensitive-information issues so the user can review them before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can print detected secret matches into terminal, CI, or agent logs.

Mitigation: Run it only in protected sessions and avoid scanning files with live credentials in shared or logged environments unless output redaction is added.

Risk: The skill should not be treated as proof that links are reachable.

Mitigation: Use it as a local syntax and pattern precheck, and verify important links with a dedicated availability checker before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lxr-666/skills/verifyguard)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text reports with severity-labeled findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include matched snippets from scanned files; protect output when checking sensitive content.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
