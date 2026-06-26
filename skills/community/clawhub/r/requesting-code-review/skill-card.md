## Description: <br>
Use when completing tasks, implementing major features, or before merging to verify work meets requirements <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlc000190](https://clawhub.ai/user/zlc000190) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to request structured code review after completing tasks, major features, bug fixes, or pre-merge work. It helps an agent collect a git range, dispatch a reviewer prompt template, and act on severity-labeled feedback about quality, testing, architecture, and readiness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to inspect git diffs and pass code-review context to a reviewer subagent, which can expose private code or secrets if used on sensitive repositories. <br>
Mitigation: Install and use it only where repository diffs may be read and shared with the reviewer subagent; check the diff for sensitive content before requesting review. <br>
Risk: An incorrect base or head SHA can cause the reviewer to assess the wrong changes. <br>
Mitigation: Verify the commit range before use, especially in private projects or changes that may contain secrets. <br>


## Reference(s): <br>
- [Code Review Agent Template](code-reviewer.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zlc000190/requesting-code-review) <br>
- [Publisher Profile](https://clawhub.ai/user/zlc000190) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured review sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholders for implementation summary, requirements or plan, base and head git SHAs, and a brief description.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
