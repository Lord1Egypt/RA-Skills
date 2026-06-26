## Description: <br>
Monitors a user's Weibo latest timeline, extracts new posts by original posting time, deduplicates by permalink, and writes a daily Markdown digest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hwb96](https://clawhub.ai/user/hwb96) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and developers with a logged-in Weibo browser profile use this skill to maintain a local Markdown digest of recent followed-account posts and reduce missed updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in Weibo browser profile and accesses Weibo timeline content. <br>
Mitigation: Install it only when local timeline monitoring is intended, and do not place account passwords, cookies, or other credentials in prompts, repositories, or output files. <br>
Risk: A recurring cron task can continue collecting local post digests after the user no longer needs background monitoring. <br>
Mitigation: Review the cron interval before installation and remove the cron entry when monitoring is no longer desired. <br>
Risk: Timeline capture may be incomplete or misleading if the latest timeline cannot be reached or post times cannot be parsed. <br>
Mitigation: Use the documented latest-timeline navigation checks, retry behavior, timestamp parsing rules, and skipped-item summary before relying on the digest. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hwb96/weibo-fresh-posts) <br>
- [Workflow reference](references/workflow.md) <br>
- [Markdown schema reference](references/markdown-schema.md) <br>
- [Cron setup reference](references/cron-setup.md) <br>
- [Weibo](https://weibo.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown digest rows, plain-text run summaries, and optional shell commands for cron setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily files under ~/weibo-digest and deduplicates rows by original post link.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
