## Description: <br>
Automated code review for security vulnerabilities, performance issues, best practices, refactoring suggestions, documentation gaps, and PR-ready comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tktk-ai](https://clawhub.ai/user/tktk-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and teams use this skill to review code or pull request diffs for security, performance, style, complexity, documentation, and concrete refactoring improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated findings or fix suggestions may be incomplete, incorrect, or unsuitable for the target repository. <br>
Mitigation: Review generated comments and code changes before applying them or relying on them for merge decisions. <br>
Risk: Code submitted for review may contain secrets, proprietary logic, or other sensitive material. <br>
Mitigation: Avoid sharing sensitive code unless the review environment and publisher are trusted for that repository. <br>
Risk: Using the skill in repository-maintenance workflows can influence public comments, artifacts, or release decisions. <br>
Mitigation: Install only if you trust the publisher with those workflows and review generated outputs before publishing or acting on them. <br>


## Reference(s): <br>
- [AI Code Reviewer on ClawHub](https://clawhub.ai/tktk-ai/tk-code-reviewer) <br>
- [tktk-ai publisher profile](https://clawhub.ai/user/tktk-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown code review report with issue lists, severity labels, file and line references, and optional corrected code snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PR-ready review comments and before/after code examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
