## Description: <br>
Slack Crawler Free helps agents inspect local Slack archive data for message search, freshness checks, bounded time slices, and read-only SQLite statistics while avoiding repeated Slack API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and Slack workspace operators use this skill to query a local Slack archive for historical messages, channel activity, freshness status, and aggregate counts. It is intended for local archive inspection rather than live Slack API synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write-capable permissions and broad action language conflict with the skill's read-only archive-search claims. <br>
Mitigation: Review before installing, restrict use to the intended local Slack archive path, and do not allow create, modify, reset, import, export, or save actions unless those file or database changes are separately reviewed. <br>
Risk: Local Slack archive results may be stale or incomplete because the free edition relies on desktop export data and does not include API sync, thread completion, or DM completion. <br>
Mitigation: Check archive freshness before answering, use bounded queries, and report date ranges, data source, and known coverage limits with results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/slack-crawler-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured text or JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include relevant workspace or channel context, absolute date ranges, counts, data freshness, and local archive limitations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
