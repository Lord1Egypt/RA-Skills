## Description: <br>
Audit failure states, retries, validation, and idempotency in the code under review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ritual](https://clawhub.ai/user/ritual) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill during code review to audit error paths, input validation, timeout and retry behavior, observability, and idempotency. It helps turn missing or weak failure handling into specific file-and-line review findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Ritual Cloud setup adds a separate external service and global CLI install beyond the standalone checklist. <br>
Mitigation: Use local standalone mode unless broader workspace context is needed; review the setup and get user approval before installing or connecting Ritual Cloud. <br>
Risk: Optional knowledge capture can write reusable OKF notes into the repository. <br>
Mitigation: Create OKF files only after explicit user approval, keep them small, and cite the supporting files or observations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ritual/review-error-handling) <br>
- [Ritual homepage](https://ritual.work) <br>
- [Open Knowledge Format overview](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prose with optional inline shell commands and optional OKF markdown notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review findings depend on the code and context provided to the agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
