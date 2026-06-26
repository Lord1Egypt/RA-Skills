## Description: <br>
Tencent Cloud Smart Advisor architecture risk inspection skill for retrieving cloud architecture details, architecture lists, directory data, risk assessment items, and recent architecture evaluation results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1ncludesteven](https://clawhub.ai/user/1ncludesteven) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud architects, operators, and engineers use this skill to query Tencent Cloud Smart Advisor architecture assets, retrieve risk checks and Well-Architected evaluation results, and generate console links for follow-up review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make high-impact Tencent Cloud IAM changes. <br>
Mitigation: Review the requested CAM permissions before installation and run role creation or cleanup --cloud only after explicit user approval. <br>
Risk: High-privilege Tencent Cloud AK/SK credentials may be exposed if persisted in shell startup files. <br>
Mitigation: Use a dedicated least-privilege sub-account or role and avoid storing high-privilege AK/SK values in shell startup files. <br>
Risk: Generated Tencent Cloud console login URLs act as temporary credentials. <br>
Mitigation: Treat generated login URLs as sensitive, time-limited credentials and regenerate them only when needed. <br>
Risk: The security summary reports permission and TLS-safety inconsistencies that require review before installation. <br>
Mitigation: Review the Tencent Cloud permissions and TLS behavior before deploying the skill in a production environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1ncludesteven/tsa-risk) <br>
- [Tencent Cloud](https://cloud.tencent.com) <br>
- [Tencent Cloud API credentials console](https://console.cloud.tencent.com/cam/capi) <br>
- [Tencent Cloud CAM role console](https://console.cloud.tencent.com/cam/role) <br>
- [Tencent Cloud Smart Advisor console](https://console.cloud.tencent.com/advisor) <br>
- [DescribeArch - architecture details](references/DescribeArch.md) <br>
- [DescribeArchList - architecture list](references/DescribeArchList.md) <br>
- [DescribeLastEvaluation - latest architecture evaluation](references/DescribeLastEvaluation.md) <br>
- [DescribeStrategies - risk assessment items](references/DescribeStrategies.md) <br>
- [ListDirectoryV2 - directory tree](references/ListDirectoryV2.md) <br>
- [ListUnorganizedDirectory - unorganized directory](references/ListUnorganizedDirectory.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown responses with shell command snippets, JSON API results, configuration guidance, and temporary console links when applicable.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials in environment variables; API calls return JSON and console login links are temporary credentials that should be regenerated for each use.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
