## Description: <br>
Analyzes GitHub projects and produces plain-language Chinese Markdown evaluation reports for repository review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liderongyao-crypto](https://clawhub.ai/user/liderongyao-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, students, and technical evaluators use this skill to assess GitHub repositories, compare alternatives, judge project health, and produce decision-oriented reports. It is intended for Chinese-language, plain-spoken analysis rather than executable code testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ambiguous project names or unclear GitHub references can lead to analysis of the wrong repository. <br>
Mitigation: Provide a clear GitHub URL or owner/repo name and verify the repository identity before relying on the report. <br>
Risk: The skill may create local Markdown report files. <br>
Mitigation: Review the output path and inspect generated reports before sharing or committing them. <br>
Risk: The report is based on public repository information and web research rather than running the target project. <br>
Mitigation: Confirm critical claims with official documentation, current repository state, and hands-on testing before making production decisions. <br>


## Reference(s): <br>
- [GitHub project analysis framework](references/analysis-framework.md) <br>
- [How to use](HOW_TO_USE.md) <br>
- [ClawHub skill page](https://clawhub.ai/liderongyao-crypto/skill-github-project-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance, Files] <br>
**Output Format:** [Chinese Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports full and quick report modes and may create a local Markdown report folder when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
