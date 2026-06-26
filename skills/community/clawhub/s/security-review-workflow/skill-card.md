## Description: <br>
Use when the current branch or PR needs a focused security review that minimizes false positives and only reports concrete, exploit-relevant issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review branch or pull request diffs for concrete security vulnerabilities. It focuses on actionable findings with severity, exploit path, and fix recommendations while filtering low-confidence noise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Branch diffs and security-relevant code context may contain private code or secrets. <br>
Mitigation: Run the skill only where sharing that code with the chosen agent or model is acceptable, and exclude secrets or unrelated private files from the review context. <br>
Risk: The workflow is intentionally focused on changed attack surfaces and may miss vulnerabilities outside the current branch or pull request diff. <br>
Mitigation: Use it as a targeted security review for changes, and pair it with broader security testing when full-codebase assurance is needed. <br>


## Reference(s): <br>
- [Security Review Workflow on ClawHub](https://clawhub.ai/wimi321/security-review-workflow) <br>
- [wimi321 ClawHub Publisher Profile](https://clawhub.ai/user/wimi321) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown report with security findings, severity, exploit path, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filters speculative and low-confidence issues; may produce no findings when evidence is insufficient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
