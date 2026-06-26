## Description: <br>
Run the pure-LLM variant of the QLCoder workflow for both CVE samples and local Web App repositories, with multi-profile taint-flow analysis for Java Web and Python Web projects without CodeQL/database build steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[setg-git](https://clawhub.ai/user/setg-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to run pure-LLM CVE sample analysis or local Java/Python web application taint-flow triage. It helps produce source, sink, sanitizer, and prioritized finding summaries for manual security review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads repositories selected for analysis and may produce reports containing local code, dependency, or configuration details. <br>
Mitigation: Run it only on repositories intended for scanning and review generated reports before sharing them. <br>
Risk: The taint-flow and finding summaries are candidate analysis and may include false positives or miss exploitable paths. <br>
Mitigation: Verify findings with manual tracing, targeted tests, or other security validation before relying on the results. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Taint Profiles](references/taint_profiles.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON, markdown] <br>
**Output Format:** [Markdown instructions with shell commands; generated analysis artifacts are JSON and Markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON artifacts are treated as the source of truth, with Markdown reports for human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
