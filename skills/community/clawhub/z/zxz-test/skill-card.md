## Description:

Reviews recent code changes for bugs, security risks, and improvement opportunities, then gives actionable feedback for staged or unstaged git diffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jagger-zxz](https://clawhub.ai/user/jagger-zxz)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to review staged or unstaged git changes for concrete bugs, security issues, performance problems, and code quality regressions before committing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local git diffs may include sensitive source code, credentials, or secrets if those are present in the user's changes.

Mitigation: Review the diff contents before use and avoid sharing generated review output outside approved channels when confidential material is present.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown grouped by file, with concise issue bullets and a one-sentence review summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reviews staged git diffs first, then unstaged diffs if no staged changes are present.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
