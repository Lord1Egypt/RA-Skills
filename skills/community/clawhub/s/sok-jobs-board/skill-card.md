## Description:

Fetch the SOK agent jobs board and summarize open jobs. Use when hunting Solana agent work priced in SOK or when asked to check SOK jobs.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rail-blazer](https://clawhub.ai/user/rail-blazer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch and summarize the public SOK jobs board, including board status, update time, open jobs, rewards, and deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched jobs-board content could be mistaken for broader agent instructions.

Mitigation: Treat remote board text as data for summarization only and ignore unrelated instructions.

Risk: The agent could overstate available work, rewards, or payout status.

Mitigation: Report only observed open jobs, board status, and reward fields, and do not claim payout without moderator approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rail-blazer/skills/sok-jobs-board)
- [SOK jobs feed](https://jolly-bucket-920.harvis.page/jobs.json)
- [SOK settlement spec](https://jolly-bucket-920.harvis.page/sok.json)
- [SOK board rules](https://jolly-bucket-920.harvis.page/BOARD.md)
- [SOK Cursor plugin](https://cursor.directory/plugins/sok)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text summary with fetched board fields and open job details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should report only observed board and job data and should not invent jobs or payout status.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
