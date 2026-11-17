## Description:

Run narrow, local pre-publish checks for an OpenClaw skill folder without dynamic shell evaluation, network access, publishing, or destructive actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use Release Guard to run local, non-destructive readiness checks on an OpenClaw skill folder before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script has a limited temporary-file safety issue when writing scan output under /tmp.

Mitigation: Do not run it as root or on hostile shared machines; prefer a patched release that uses mktemp-based private temporary files before relying on it in sensitive environments.

Risk: The checker can only report common release-readiness risks and is not a full security audit.

Mitigation: Use its WARN and FAIL output as review prompts, then complete manual review before publishing.

## Reference(s):

- [Release Checklist](references/checklist.md)
- [ClawHub Release Page](https://clawhub.ai/harrylabsj/skills/release-guard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Compact Markdown-style report with PASS/WARN/FAIL lines, final status, files to review, and recommended next steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs against a user-selected local skill folder and reports findings without publishing, modifying files, installing dependencies, or contacting external services.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
