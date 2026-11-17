## Description:

Git hook to detect secrets before commit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to install or run a local git pre-commit scanner that checks staged files or specified paths for common credential patterns before committing code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detected credentials may appear in terminal or CI logs.

Mitigation: Run only in controlled environments until matched secret values are redacted, and avoid publishing scan logs.

Risk: Installing the hook can overwrite an existing pre-commit hook.

Mitigation: Review the repository's current hook before installation and merge this scanner into existing hook logic when needed.

Risk: Staged-content scanning can be bypassed or miss content.

Mitigation: Use this as a local guard alongside CI or server-side secret scanning, and confirm staged-blob scanning and exit-code behavior before relying on it.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text status messages plus JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit a non-zero exit code when a staged scan finds secrets.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
