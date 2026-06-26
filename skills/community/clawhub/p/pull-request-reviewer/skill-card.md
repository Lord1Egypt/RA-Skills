## Description: <br>
Reviews pull requests and code diffs for logic bugs, security risks, missing tests, breaking API changes, performance issues, and maintainability concerns before merge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lnguyen1996](https://clawhub.ai/user/Lnguyen1996) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review git diffs, pull request URLs, or pasted code changes and receive a prioritized merge-readiness report. It is intended to surface critical correctness, security, testing, API, performance, and style issues before code is merged. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review findings may include false positives, false negatives, or incomplete recommendations for a specific codebase. <br>
Mitigation: Treat the report as review assistance and require human reviewer confirmation before merging or changing production code. <br>
Risk: Pull request URLs, diffs, or pasted code can contain confidential source code, credentials, or sensitive business context. <br>
Mitigation: Share only code and repository links that the agent is authorized to access, and remove secrets before submitting review input. <br>
Risk: Suggested fixes may alter behavior, public APIs, or security boundaries if applied without project context. <br>
Mitigation: Validate suggested changes with the project test suite, security review, and compatibility checks before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lnguyen1996/pull-request-reviewer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown structured as block-merge findings, warnings, suggestions, approvals, and summary, with code snippets when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prioritizes block-merge issues before warnings and style suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
