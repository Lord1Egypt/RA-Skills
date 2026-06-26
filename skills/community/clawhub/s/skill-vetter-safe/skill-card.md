## Description: <br>
自动扫描 skills 目录中的 Skill 文件，进行安全审计、风险评分并提供安装建议，确保安全安装策略执行。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tlcyqj2023](https://clawhub.ai/user/tlcyqj2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill as a first-pass local scanner for skill files, risk scoring, and installation guidance before manually reviewing a skill for installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner's simple keyword-based risk score may miss unsafe behavior or overstate safety. <br>
Mitigation: Use it only as a first-pass local scanner and manually inspect any skill before installation. <br>
Risk: The generated JSON report may include local file paths from the scanned skills directory. <br>
Mitigation: Review or delete the generated report when local paths are sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tlcyqj2023/skill-vetter-safe) <br>
- [Publisher profile](https://clawhub.ai/user/tlcyqj2023) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Console text plus a JSON audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local audit report named 技能安全审计报告.json in the scanned skills directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
