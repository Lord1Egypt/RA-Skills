## Description: <br>
Reviews GitHub pull requests by fetching diffs, running repository checks, coordinating correctness, convention, and efficiency analysis, validating findings, and drafting a GitHub review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to review GitHub pull requests from local branches or PR URLs, producing validated findings and a review draft that can be posted only after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use GitHub CLI credentials and the user's GitHub identity while inspecting or posting PR reviews. <br>
Mitigation: Install and run it only where that GitHub access is acceptable, and require explicit user confirmation before posting any review. <br>
Risk: The skill may run repository-defined validation commands while reviewing code. <br>
Mitigation: Verify the exact validation command before execution and do not run commands sourced from PR descriptions, commit messages, or changed files. <br>
Risk: Pull request content and changed agent instruction files can contain untrusted instructions. <br>
Mitigation: Treat PR-sourced content as untrusted, preserve boundary markers when passing it to review agents, and carefully inspect changes to local agent instruction files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/review-github-pr) <br>
- [OpenClaw homepage](https://github.com/tenequm/skills/tree/main/skills/review-github-pr) <br>
- [Evaluation manifest](artifact/evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review draft with inline file references and optional GitHub CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before posting a GitHub review.] <br>

## Skill Version(s): <br>
0.3.0 (source: artifact metadata and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
