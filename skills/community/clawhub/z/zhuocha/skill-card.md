## Description:

zhuocha helps agents verify whether bid records grouped under the same reid are true duplicates by comparing project identifiers, customers, procurement details, source text, and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cybluesky](https://clawhub.ai/user/cybluesky)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or operations analysts use this skill to review procurement and bid deduplication groups, decide whether grouped jy_id records represent true duplicates, and prepare result-table writebacks after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to make persistent writebacks to internal duplicate-review result tables.

Mitigation: Require an explicit preview-and-confirm step before any insert and retain enough audit detail to review each duplicate decision.

Risk: The documented recovery path includes a full-table TRUNCATE operation if bad rows are inserted.

Mitigation: Remove or tightly gate any full-table truncation workflow and prefer scoped correction procedures.

Risk: The workflow depends on internal HTTP services and SQL-bearing API payloads.

Mitigation: Use the skill only in a trusted internal database environment, prefer authenticated HTTPS or another protected channel, and scope or parameterize queries wherever the service allows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cybluesky/skills/zhuocha)
- [ClawHub publisher profile](https://clawhub.ai/user/cybluesky)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown summaries with optional Python snippets and JSON API writeback payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce duplicate/non-duplicate decisions, retained/deleted jy_id lists, reasoning, batch totals, and guarded database writeback instructions.]

## Skill Version(s):

1.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
