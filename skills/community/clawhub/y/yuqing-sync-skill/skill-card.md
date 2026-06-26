## Description: <br>
从慧科/小爱数据接口增量拉取舆情数据，并写入飞书多维表，支持字段准备、去重和自动分表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankieway](https://clawhub.ai/user/frankieway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, public-opinion, or data teams use this skill to sync recent Huike/Xiaoai monitoring records into a Feishu Bitable for tracking, review, and downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Feishu app credentials and a Huike/Xiaoai bearer token. <br>
Mitigation: Use a dedicated least-privilege Feishu app, store credentials only in the runtime secret mechanism, and rotate tokens if they may have been exposed. <br>
Risk: The skill has remote write authority for the configured Feishu Bitable and can create fields, insert records, and create a new table when capacity is reached. <br>
Mitigation: Test against a non-production Bitable first, verify the Bitable URL before each deployment, and limit the Feishu app to only the intended workspace and base. <br>
Risk: Local .cache files may contain a short-lived Feishu tenant token and sync metadata. <br>
Mitigation: Run the skill in an isolated workspace, avoid committing cache files, and clear the cache after use in shared environments. <br>
Risk: The Xiaoai base URL can be overridden, and the artifact default uses an HTTP endpoint. <br>
Mitigation: Only override the endpoint to a trusted destination and prefer an HTTPS Huike/Xiaoai endpoint if one is available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frankieway/yuqing-sync-skill) <br>
- [Publisher profile](https://clawhub.ai/user/frankieway) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text] <br>
**Output Format:** [Plain text status output with inserted_count=<integer>] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes mapped records to a target Feishu Bitable, prepares missing fields, skips existing records by md5_doc_id, and may create a new table when the current table reaches the configured record limit.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
