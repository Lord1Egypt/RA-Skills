## Description: <br>
Use when completing tasks, implementing major features, or before merging to verify work meets requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouzy-creator](https://clawhub.ai/user/zhouzy-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to request focused SVN-based code reviews after tasks, before major merges, or when a fresh technical assessment is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SVN diffs may expose source code or sensitive implementation details to an agent review context. <br>
Mitigation: Use the skill only on code that is appropriate to share with the configured review agent and review context. <br>
Risk: An incorrect SVN revision range can produce an incomplete or overly broad review. <br>
Mitigation: Confirm the base and head revisions before dispatching the review request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouzy-creator/svn-code-review) <br>
- [Code review agent template](code-reviewer.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline SVN shell commands and review-template placeholders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a focused code-review request and expected review structure; no API calls or credentials are required by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter; release metadata version 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
