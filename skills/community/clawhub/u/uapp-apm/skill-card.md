## Description: <br>
Queries Umeng U-APM crash, stability, startup, network, native page, H5 page, and minute-level performance data through read-only umeng-cli calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squall0925](https://clawhub.ai/user/squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to query read-only Umeng APM metrics for app stability, startup latency, network performance, page performance, and minute-level incidents when investigating crashes or performance regressions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes under-disclosed telemetry that may send app-specific identifiers outside the requested analysis workflow. <br>
Mitigation: Review telemetry behavior before installing or using the skill, and avoid sensitive production app identifiers unless the publisher documents what is sent, where it goes, and how to disable it. <br>
Risk: The skill requires Umeng authentication and app identifiers to query APM data. <br>
Mitigation: Use least-privilege accounts, confirm commands are read-only before execution, and avoid sharing credentials or app keys in logs or public outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/squall0925/uapp-apm) <br>
- [Umeng CLI Homepage](https://github.com/umeng/umeng-cli) <br>
- [Umeng API Credentials Documentation](https://devs.umeng.com/api/credentials) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires umeng-cli authentication and app dataSourceId values; documented API calls are read-only.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
