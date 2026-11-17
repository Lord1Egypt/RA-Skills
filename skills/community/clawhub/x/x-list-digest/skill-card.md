## Description:

On request, this skill collects authorized X lists within a fixed time window, skips archived posts, and produces daily market-writing digests and weekly off-topic statistics, with optional Feishu archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and content teams use authorized X lists to prepare source-backed daily writing reports, track market viewpoints, and optionally archive reports to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Collection accesses a logged-in X session and authorized lists.

Mitigation: Confirm browser access and the intended lists before running; use only the authorized host browser.

Risk: Optional Feishu archiving creates or updates documents under the user's profile.

Mitigation: Use only a user-authorized CLI profile and destination, and verify written documents by readback.

Risk: Local source evidence and reports persist, and scheduling can trigger later runs.

Mitigation: Choose the data directory deliberately and enable scheduling only with separate explicit consent.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/0xcjl/skills/x-list-digest)
- [Host adapters](artifact/references/agent-adapters.md)
- [Collection contract](artifact/references/collector.md)
- [Native Feishu CLI archive](artifact/references/feishu-cli.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Guidance]

**Output Format:** [Chat summary and Markdown reports, with local archive files and optional Feishu documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily reports include source references; weekly off-topic statistics are included when applicable.]

## Skill Version(s):

2.0.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
