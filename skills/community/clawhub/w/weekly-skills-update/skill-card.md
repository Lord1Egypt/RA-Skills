## Description:

Automatically updates installed skills when triggered, refreshes the skills index when needed, and sends a concise update summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ken0122](https://clawhub.ai/user/ken0122)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run a periodic maintenance workflow that updates installed ClawHub skills, summarizes update results, and records index changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can bulk-update all installed skills and modify local skill index or log files without confirmation, version pinning, staging, or rollback guidance.

Mitigation: Run it only when broad updates are intended, back up the current skill directory and index first, and review pending updates before accepting the results.

Risk: A global update may introduce unwanted or unstable skill changes.

Mitigation: Prefer pinned or allowlisted updates and add a confirmation step before applying changes.

Risk: The workflow writes update output to a temporary file.

Mitigation: Use a secure temporary file location and avoid exposing logs that may contain sensitive local paths or command output.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with inline shell commands and status counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local skill index and log files as part of the workflow.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
