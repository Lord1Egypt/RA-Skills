## Description: <br>
Manage West.cn DNS records by adding, modifying, or deleting A, CNAME, MX, TXT, and AAAA records through the West.cn API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[missKivin](https://clawhub.ai/user/missKivin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to let an agent manage live West.cn DNS records for domains they administer. It is suited for controlled DNS maintenance workflows where add, modify, and delete operations are reviewed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can directly change or delete live DNS records using West.cn API credentials. <br>
Mitigation: Use least-privilege API credentials where available, verify every domain and record before modify or delete actions, and keep a rollback plan or DNS backup. <br>
Risk: The API password is provided to the agent at runtime and could be exposed through prompts, logs, or configuration files. <br>
Mitigation: Keep the API password out of prompts, logs, and stored configuration, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/missKivin/west-dns-manager) <br>
- [West.cn domain API endpoint](https://api.west.cn/api/v2/domain/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response with success, message, data, and error fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns standardized operation status and API response data for DNS record changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
