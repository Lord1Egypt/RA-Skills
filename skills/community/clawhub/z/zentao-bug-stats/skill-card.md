## Description: <br>
统计禅道中指定起始日期的版本Bug数量，以及今日新建、关闭、激活和问题引入的Bug数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanweify](https://clawhub.ai/user/hanweify) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA, engineering, and release teams use this skill to collect ZenTao bug counts for daily reporting and version-date summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports embedded default ZenTao credentials and a plain HTTP internal ZenTao URL. <br>
Mitigation: Review before installing, treat the exposed password as compromised, set your own ZenTao URL and credentials explicitly, require HTTPS where possible, and use an account limited to the read access needed for bug statistics. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hanweify/zentao-bug-stats) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration] <br>
**Output Format:** [Console text from a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZenTao URL and credentials supplied through arguments or environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
