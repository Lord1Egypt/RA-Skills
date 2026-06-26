## Description: <br>
Self Evolution Engine helps skill developers monitor execution logs and user feedback, analyze failures and performance, and generate improvement proposals for ongoing skill maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to inspect skill execution data, error patterns, and feedback, then produce improvement proposals, patch templates, reports, and version-management actions for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes paid billing behavior that can charge an external SkillPay account using an environment-derived user ID without a clear per-call consent step. <br>
Mitigation: Install only when paid execution is intended; review or disable payment.py, avoid setting SKILLPAY_USER_ID unless the charge path is understood, and confirm billing before use. <br>
Risk: The artifact requires sensitive billing credentials and includes an embedded billing key. <br>
Mitigation: Rotate or remove the embedded billing key and use explicitly managed credentials before running the skill. <br>
Risk: Evolution and version-management scripts can create, copy, restore, or modify files in selected skill directories. <br>
Mitigation: Run file-changing commands only against test or explicitly chosen skill directories and review generated changes before applying them. <br>


## Reference(s): <br>
- [Architecture Design](references/architecture.md) <br>
- [SkillPay Billing Provider](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown, JSON reports, code patch templates, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local log, evolution, backup, and version snapshot files when its scripts are run.] <br>

## Skill Version(s): <br>
2025.4.15 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
