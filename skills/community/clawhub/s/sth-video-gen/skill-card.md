## Description:

Generate vertical 9:16 videos for Sing The Hook song templates using a two-stage pipeline with MCP, trimming, uploading to GCS, and database updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuyinzhuyin](https://clawhub.ai/user/zhuyinzhuyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to process CSV-listed Sing The Hook song templates, generate lip-synced vertical videos, and record resulting video URLs and statuses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send data to outside services, upload media, and modify PostgreSQL records.

Mitigation: Install and run it only in controlled staging or approved production environments with explicit operator approval before uploads or database updates.

Risk: CSV input, database URLs, and MCP responses may be untrusted.

Mitigation: Require preview or dry-run review, validate inputs and returned URLs, and add SQL parameterization and URL allowlisting before broad production use.

Risk: Database, MCP, and GCS credentials could grant more access than the workflow requires.

Mitigation: Use least-privilege PostgreSQL and GCS credentials and avoid production API keys or broad database accounts until rollback controls are clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuyinzhuyin/skills/sth-video-gen)
- [Publisher profile](https://clawhub.ai/user/zhuyinzhuyin)
- [MCP fetch-asset endpoint examples](artifact/fetch_asset_examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline bash commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow can generate video URLs, update CSV status fields, upload media, and update PostgreSQL records.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
