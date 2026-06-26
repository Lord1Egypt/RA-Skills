## Description: <br>
AI-powered code analysis via LogicArt for bug detection, security review, code quality analysis, and logic flow visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review code snippets or files for bugs, security issues, complexity, suggested fixes, and logic flow before relying on or shipping the code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Code sent to external analysis services may expose proprietary logic, customer data, or embedded credentials. <br>
Mitigation: Confirm the exact snippet or file before transmission, scan for secrets, remove sensitive data, and avoid repository-wide scans unless the broader scope has been reviewed and approved. <br>
Risk: Automated review pipelines can transmit code repeatedly without human oversight. <br>
Mitigation: Require per-invocation approval for each external transmission, or use a manual trigger or local-only review approach for automated workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/quack-code-review-hardened) <br>
- [LogicArt analysis API](https://logic.art/api/agent/analyze) <br>
- [Validate Repo](https://validate-repo.replit.app) <br>
- [Safety evaluation](SAFETY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON analysis responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results prioritize critical bugs and security issues, then complexity, suggestions, and logic flow when provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
