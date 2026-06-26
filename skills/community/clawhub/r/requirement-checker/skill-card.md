## Description: <br>
Checks requirement documents with an LLM and produces prioritized improvement suggestions, source quotes, GWT acceptance criteria, and optional batch summary reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gotomanutd-dot](https://clawhub.ai/user/gotomanutd-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, analysts, and development teams use this skill to review requirement documents for completeness, clarity, exception handling, integration details, and testable acceptance criteria before review or delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requirement document contents may be sent to the configured LLM provider. <br>
Mitigation: Use the skill only with documents approved for that provider, and review the configured base URL before running checks. <br>
Risk: API keys may be read from environment or OpenClaw configuration and may be saved in config.json. <br>
Mitigation: Use scoped non-production keys where possible, avoid broad credentials, and verify file permissions on config.json. <br>
Risk: The install flow may modify the Python environment. <br>
Mitigation: Prefer manual dependency installation in a virtual environment when you need tighter control over installed packages. <br>
Risk: Generated requirement-review reports may contain sensitive source-document excerpts. <br>
Mitigation: Store reports in an approved location and apply the same access controls used for the original requirement documents. <br>


## Reference(s): <br>
- [Requirement Checker ClawHub page](https://clawhub.ai/gotomanutd-dot/requirement-checker) <br>
- [Requirement Specification Checklist](references/checklist.md) <br>
- [LLM Enhancement Notes](references/llm-enhanced.md) <br>
- [Requirement Document Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and summary text with configuration prompts and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce per-document reports and an optional batch summary report.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release evidence and ClawHub metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
