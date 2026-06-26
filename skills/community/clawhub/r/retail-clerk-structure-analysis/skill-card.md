## Description: <br>
导购结构分析工具，用于分析门店导购表现结构并识别导购波动对门店业绩波动的贡献度。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwyang7](https://clawhub.ai/user/gwyang7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail operators, analysts, and agent workflows use this skill to evaluate clerk sales distribution, identify top/mid/tail performers, attribute store performance changes to individual clerks, and select drill-down targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses store and employee performance data through an undeclared API client. <br>
Mitigation: Run it only with explicit authorization for the relevant store data, and require documented credentials, scopes, and access controls before deployment. <br>
Risk: The artifact loads local code through a developer-specific import path, which may execute unreviewed code outside the packaged skill. <br>
Mitigation: Package or declare the API client dependency and remove developer-local import paths before installing in a shared or production agent environment. <br>
Risk: The server security verdict is suspicious and VirusTotal was pending in the provided evidence. <br>
Mitigation: Review the artifact and repeat security scanning before installation or runtime use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gwyang7/retail-clerk-structure-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Analysis, Guidance] <br>
**Output Format:** [JSON-like Python dictionary containing structure metrics, clerk contributions, key-person lists, drill-down targets, findings, and total change.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally print a verbose text report while returning structured analysis data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
