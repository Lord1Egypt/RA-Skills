## Description:

Stranger Suite tests whether README setup instructions and API documentation are sufficient for a new user or agent to complete a task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT

## Use Case:

Developers use Fresh-Eyes to check whether a newcomer can follow a project's README and use Stranger API to see whether API documentation is enough to complete a specified task against a local sandbox API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because a referenced local path was unavailable, and the Git-based install command received a disputed signature match despite a benign verdict.

Mitigation: Review the install source before use and run project commands only in a disposable environment; treat the scanner verdict as an assessment, not a guarantee.

## Reference(s):

- [Stranger Suite project repository](https://github.com/RakTikoo/stranger-suite)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Files]

**Output Format:** [JSON summary and Markdown report, with a corrected README draft for Fresh-Eyes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes report.md in the requested output folder.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
