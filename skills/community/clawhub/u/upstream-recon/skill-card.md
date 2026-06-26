## Description: <br>
Investigate an open-source project before interacting with it through PRs, issues, or comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SeMmyT](https://clawhub.ai/user/SeMmyT) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill before filing issues, submitting pull requests, or commenting on open-source repositories. It helps them review existing issues and pull requests, maintainer response patterns, merge velocity, and topic overlap before choosing the next action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read public GitHub issues, pull requests, comments, and repository metadata through the GitHub CLI. <br>
Mitigation: Install only from a trusted source and review the proposed GitHub CLI commands before use. <br>
Risk: Follow-up actions such as opening an issue, submitting a pull request, or posting a comment can affect a user's GitHub account or an upstream project. <br>
Mitigation: Keep those write actions under explicit user control; the skill should advise on them rather than perform them without direction. <br>


## Reference(s): <br>
- [Claude Code skills documentation](https://docs.anthropic.com/en/docs/claude-code/skills) <br>
- [ClawHub skill page](https://clawhub.ai/SeMmyT/upstream-recon) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown report with recommendation labels and concrete next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GitHub CLI queries to inspect public repository metadata, issues, pull requests, comments, and contributor patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
