## Description: <br>
Online (real-time) data analysis, rule extraction, and pattern recognition for testing scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shineniefei](https://clawhub.ai/user/shineniefei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to analyze logs, API responses, streams, or database exports, extract business rules, identify testing patterns, and produce anomaly reports for test design. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include business data, personal data, tokens, or other sensitive values from logs, API responses, or database exports. <br>
Mitigation: Sanitize or redact inputs before analysis and handle generated reports as sensitive artifacts. <br>
Risk: The skill runs local Python scripts against user-selected files and depends on numpy. <br>
Mitigation: Run it in a trusted Python environment and only execute the scripts on files you intend to analyze. <br>
Risk: Automatically extracted rules, test suggestions, and anomaly classifications can be incomplete or misleading. <br>
Mitigation: Review extracted findings before using them for test coverage, business-rule documentation, or release decisions. <br>


## Reference(s): <br>
- [Rule Extraction Standards](references/rule_extraction_standards.md) <br>
- [ClawHub Release Page](https://clawhub.ai/shineniefei/test-online-analysis) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports and concise text guidance, with optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include extracted rules, test case suggestions, anomaly severity, and values copied from analyzed input data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
