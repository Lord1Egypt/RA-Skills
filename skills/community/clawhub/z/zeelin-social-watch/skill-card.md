## Description: <br>
Zeelin Social Watch helps agents monitor social media sentiment, trending events, platform rankings, and account data through the GSData open platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thu-nmrc](https://clawhub.ai/user/thu-nmrc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to query GSData for social media sentiment, hot events, platform rankings, content search, and account data. It supports read-only monitoring by default and requires explicit confirmation for write-like warning, ranking-group, and tracked-account actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes raw or write-like GSData actions that can change warning rules, recipient emails, custom ranking groups, or tracked accounts. <br>
Mitigation: Run dry-run checks first, require explicit user confirmation before write-like actions, append --allow-write only after approval, and review the exact route and parameters before execution. <br>
Risk: Authenticated requests use a plaintext HTTP base URL by default. <br>
Mitigation: Prefer an HTTPS GSDATA_BASE_URL if GSData supports it, avoid using credentials over untrusted networks, and confirm transport security before handling sensitive monitoring data. <br>
Risk: GSData credentials give the agent access to the user's GSData account. <br>
Mitigation: Use environment variables for GSDATA_APP_KEY and GSDATA_APP_SECRET, avoid hardcoded keys, prefer least-privilege credentials, and rotate or revoke keys if exposure is suspected. <br>
Risk: Large API responses can flood chat context or hide important details. <br>
Mitigation: Use small page sizes for conversational answers, respect the API maximum of 20 items per page, probe total counts before pagination, and summarize key fields before showing raw data. <br>


## Reference(s): <br>
- [Zeelin Social Watch ClawHub page](https://clawhub.ai/thu-nmrc/zeelin-social-watch) <br>
- [Publisher profile](https://clawhub.ai/user/thu-nmrc) <br>
- [GSData API base endpoint](http://databus.gsdata.cn:8888/api/service) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown summaries with shell commands and selected JSON fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only by default; write-like actions require explicit confirmation and --allow-write; chat responses should use small page sizes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter declares 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
