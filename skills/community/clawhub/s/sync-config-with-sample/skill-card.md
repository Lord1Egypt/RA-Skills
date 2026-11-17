## Description:

Syncs a production config file against the latest upstream sample by copying only reference comments while preserving live settings and leaving only real configuration differences visible in diffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when maintaining a live configuration file beside a freshly downloaded upstream sample. It helps classify diff hunks, copy only inert reference comments, preserve user configuration, and produce a final diff for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to guide edits to a production configuration file.

Mitigation: Review the final diff before accepting changes and confirm that the sample file is unmodified, no live settings changed, and only real configuration differences remain.

Risk: Ambiguous upstream changes, such as renames or deprecations, can look like ordinary configuration differences.

Mitigation: Investigate ambiguous hunks against the sample, upstream project history, and the installed version, then get user confirmation before applying any edit.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with diff summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes hunk classifications, recommended edits, final diff review, and a list of preserved configuration differences.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
