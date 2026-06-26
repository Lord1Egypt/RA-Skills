## Description: <br>
验证XML文件是否为中国数电票（全面数字化电子发票）格式，检查XML结构、必需字段和数电票特征。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanw2039](https://clawhub.ai/user/hanw2039) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, finance teams, and invoice-processing agents use this skill to screen XML files for expected China fully digital electronic invoice structure and produce clear pass/fail validation guidance. It is suitable for quick local checks before deeper tax, accounting, or compliance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included validator is incomplete and could be mistaken for authoritative tax or compliance proof. <br>
Mitigation: Use it as a quick local screening helper only, and rely on an official schema, validated parser, and domain review before trusting a pass result for tax, accounting, or compliance decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanw2039/validate-einvoice-xml) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, markdown] <br>
**Output Format:** [Markdown with an inline Python validation script and report template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces validation guidance and pass/fail reporting for XML invoice files; no network access or persistent storage is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
