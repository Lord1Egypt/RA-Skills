## Description: <br>
Production development workflow with TODO tracking, Graphite PRs, GitHub issues, Vercel deploy checks, and SMS notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelmonetized](https://clawhub.ai/user/michaelmonetized) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to run production development tasks with tracked TODOs, changelog updates, staged-diff review, Graphite pull requests, GitHub issues, deployment checks, and concise completion reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can affect source repositories and developer services through staging, pull request, issue, and deployment commands. <br>
Mitigation: Confirm the target repository and accounts, inspect staged diffs before submission, and review issue and PR text before publishing. <br>
Risk: Local command aliases or tools used by the workflow could resolve to unexpected executables. <br>
Mitigation: Verify that gt, gh, vl, and vercel resolve to trusted local tools before using the workflow. <br>


## Reference(s): <br>
- [Graphite](https://graphite.dev) <br>
- [GitHub CLI](https://cli.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and task templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes workflow steps, branch naming conventions, issue and PR command examples, deployment-check guidance, and SMS-ready reporting text.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
