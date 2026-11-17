## Description:

Intelligent git commit assistant that analyzes diffs, enforces conventional commits, detects common secret patterns, and generates meaningful commit messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nakedoshadow](https://clawhub.ai/user/nakedoshadow)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill to review repository changes, run local git safety checks, prepare explicit staging choices, and create conventional commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can stage files and create local git commits when used on broad commit-related triggers.

Mitigation: Review the proposed file list and commit message before allowing any write action.

Risk: The built-in grep-based secret scan may print secret-like values in terminal output.

Mitigation: Run the scan only in a secure terminal where output is not logged or shared.

Risk: The built-in secret scan may miss obfuscated secrets or produce false positives.

Mitigation: Use a dedicated scanner such as gitleaks or trufflehog for high-security repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nakedoshadow/skills/shadows-smart-commit)
- [ClawHub homepage metadata](https://clawhub.ai/NakedoShadow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline git commands and proposed commit text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local git workflow guidance with proposed files to stage, security scan results, commit message, and post-commit status.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
