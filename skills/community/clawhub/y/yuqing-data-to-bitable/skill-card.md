## Description: <br>
Incrementally pulls public-opinion records from the XiaoAi data API and writes mapped records into Feishu Bitable, including field creation, duplicate checks, and case ID assignment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FrankieWay](https://clawhub.ai/user/FrankieWay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to sync XiaoAi public-opinion monitoring data into a Feishu Bitable for review, reporting, and downstream tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can repeatedly modify Feishu Bitable data. <br>
Mitigation: Run it manually against a test Bitable first, then use least-privileged Feishu credentials and confirm the intended schedule before enabling recurring sync. <br>
Risk: The skill depends on XiaoAi and Feishu secrets and stores operational cache files locally. <br>
Mitigation: Protect the .env and .cache directories, avoid passing secrets on the command line where possible, and rotate credentials if logs or caches are exposed. <br>
Risk: Background cron or long-running execution can continue syncing after installation. <br>
Mitigation: Confirm whether any cron job or persistent process is enabled and disable it until the target Bitable, credentials, and time window are verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FrankieWay/yuqing-data-to-bitable) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/FrankieWay) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text status output, shell commands, JSON status files, and Feishu Bitable record updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emits inserted_count, writes local logs/status/cache files, and modifies the configured Feishu Bitable.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact _meta.json; README_ENHANCED.md also states version 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
