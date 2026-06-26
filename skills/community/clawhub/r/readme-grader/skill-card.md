## Description: <br>
Evaluate a README file text, score it out of 100, and provide specific, actionable improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunny0826](https://clawhub.ai/user/sunny0826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and documentation reviewers use this skill to evaluate pasted README text against open-source documentation best practices and receive a score, score breakdown, strengths, improvement suggestions, and example Markdown improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: README text may contain secrets or private project information. <br>
Mitigation: Remove secrets and private information before sharing README content with the skill. <br>
Risk: Fetching README content from URLs can expose the agent to indirect prompt injection. <br>
Mitigation: Paste raw README text directly and do not fetch external README URLs at runtime. <br>
Risk: Documentation scores and suggestions may be subjective or incomplete for a project's audience. <br>
Mitigation: Review recommendations before applying them to public project documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunny0826/readme-grader) <br>
- [Publisher profile](https://clawhub.ai/user/sunny0826) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Structured Markdown report, primarily in Chinese, with a numeric score, category breakdown, strengths, improvement suggestions, and an example README snippet.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the user to provide raw README text directly; URL-only requests should be redirected to paste the README content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
