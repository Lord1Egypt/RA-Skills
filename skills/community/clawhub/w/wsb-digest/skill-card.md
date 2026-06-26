## Description: <br>
Automatically fetches r/wallstreetbets hot-stock data, generates a daily Markdown report, and posts it to Discord with message chunking for Discord limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mingkko](https://clawhub.ai/user/Mingkko) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and operators use this skill to automate a scheduled WallStreetBets stock-trend digest for a configured Discord channel. It is intended for informational monitoring and does not provide investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scheduled trigger can repeatedly post to the configured Discord channel if cron is enabled with the wrong channel ID, binary path, or local skill path. <br>
Mitigation: Review both scripts, set the Discord channel ID and OpenClaw path manually, run a manual test, and confirm the cron entry points to the reviewed local copy before enabling the schedule. <br>
Risk: Running the cron job as root increases impact if local configuration or script contents are changed later. <br>
Mitigation: Run the job under a least-privilege user where possible and remove the crontab entry when automatic Discord posts are no longer needed. <br>
Risk: The generated stock digest could be mistaken for financial advice. <br>
Mitigation: Keep the report's informational-use disclaimer visible and treat the ApeWisdom data as a monitoring signal, not investment guidance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Mingkko/wsb-digest) <br>
- [Publisher Profile](https://clawhub.ai/user/Mingkko) <br>
- [Project Homepage](https://github.com/mingkko/wsb-digest) <br>
- [ApeWisdom WallStreetBets API](https://apewisdom.io/api/v1.0/filter/wallstreetbets) <br>
- [WSB Digest 安装指南](references/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON containing a Markdown digest; Discord delivery uses chunked Markdown messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public ApeWisdom data with retries and splits long Discord messages to stay below character limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
