## Description:

Monitor download counts for your ClawHub-published skills, track changes over time, generate daily, weekly, and monthly reports, and push notifications via Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsag1](https://clawhub.ai/user/tsag1)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub publishers and developers use this skill to monitor skill download counts, maintain local history, generate trend reports, and optionally send Feishu notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu credentials may be exposed if stored in a broadly readable .env file.

Mitigation: Use environment variables or a tightly permissioned .env file containing only CLAWHUB_FEISHU_APP_ID, CLAWHUB_FEISHU_APP_SECRET, and CLAWHUB_FEISHU_USER_OPEN_ID.

Risk: Scheduled runs can repeatedly execute the tracker and write local history.

Mitigation: Review the launchd or cron configuration before enabling scheduled collection, and keep tracker data directory permissions limited to the intended user.

Risk: The tracker runs clawhub inspect for every monitored slug and records local download history.

Mitigation: Monitor only intended skill slugs and review the generated CSV, JSON, log, and report files under ~/.openclaw/workspace/data/clawhub-tracker.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tsag1/skills/skill-download-tracker)
- [Publisher profile](https://clawhub.ai/user/tsag1)
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu message endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text output and archived Markdown reports with optional Feishu text notifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local CSV/JSON state and report archives under ~/.openclaw/workspace/data/clawhub-tracker.]

## Skill Version(s):

1.584.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
