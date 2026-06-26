## Description: <br>
Detects AI-generated writing patterns in developer text such as docs, docstrings, commit messages, PR descriptions, and code comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review repository prose, code comments, docstrings, commit messages, and PR descriptions for AI-like writing patterns and clearer wording. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read repository text files, commit messages, and GitHub PR descriptions while reviewing AI-like wording. <br>
Mitigation: Run it only in repositories and PRs where that review scope is acceptable. <br>
Risk: The skill writes a local .beagle report file that may contain excerpts and review findings. <br>
Mitigation: Review the report before sharing or committing it, especially when scanned text may be sensitive. <br>
Risk: GitHub PR description review can require an authenticated GitHub CLI session. <br>
Mitigation: Use the minimum appropriate account access and avoid running PR review commands where OAuth-backed access is not intended. <br>


## Reference(s): <br>
- [Code Documentation Patterns](references/code-docs-patterns.md) <br>
- [Communication Patterns](references/communication-patterns.md) <br>
- [Content Patterns](references/content-patterns.md) <br>
- [Filler Patterns](references/filler-patterns.md) <br>
- [Formatting Patterns](references/formatting-patterns.md) <br>
- [Vocabulary Patterns](references/vocabulary-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with a local JSON report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes .beagle/ai-writing-review.json when findings are produced; may inspect repository text, git history, and GitHub PR descriptions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
