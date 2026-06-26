## Description: <br>
Performs static codebase analysis and generates comprehensive QA, security testing, compliance, and tooling strategy reports for software repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shifulegend](https://clawhub.ai/user/shifulegend) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, security reviewers, and audit teams use this skill to inspect a repository and produce an independent testing strategy, risk assessment, and compliance-oriented QA plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads repository contents and writes reports to the local filesystem. <br>
Mitigation: Run it only on repositories you are authorized to analyze, use an output path you control, and avoid invoking it from directories that contain unrelated sensitive files. <br>
Risk: Remote repository analysis may use git network access and private repository credentials. <br>
Mitigation: Use approved remotes and read-only credentials for private repositories. <br>
Risk: Generated QA, security, and compliance conclusions are advisory and may contain unsupported or overconfident findings. <br>
Mitigation: Independently review the generated report before using it for security decisions, compliance evidence, or release gating. <br>


## Reference(s): <br>
- [QA Architecture Auditor ClawHub page](https://clawhub.ai/shifulegend/qa-architecture-auditor) <br>
- [Testing Methodologies Reference](references/methodologies.md) <br>
- [Risk Assessment Reference](references/risk-assessment.md) <br>
- [Tooling Matrix Reference](references/tooling-matrix.md) <br>
- [Compliance Frameworks Reference](references/compliance-frameworks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [HTML or Markdown report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports to a user-selected local output path; HTML output also creates a Markdown report with the same stem.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
