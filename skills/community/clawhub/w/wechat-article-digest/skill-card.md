## Description:

Fetches WeChat public-account articles, summarizes them, assigns categories, and generates a daily reading digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[milesnee](https://clawhub.ai/user/milesnee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process shared mp.weixin.qq.com article links, produce short article summaries, categorize reading material, and compile a same-day reading digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches user-supplied WeChat links through a shell curl pipeline.

Mitigation: Review before installing, run only in a constrained environment, and prefer a shell-free validated fetch path such as web_fetch.

Risk: The skill stores article reading history in local memory files with limited safeguards.

Mitigation: Confirm that saved article links and summaries are appropriate for the environment and periodically review or delete local memory records.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown responses with optional shell command execution and local markdown memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes article records to memory/YYYY-MM-DD.md and may reply NO_REPLY when no daily articles exist.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
