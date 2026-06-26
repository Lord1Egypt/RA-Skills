## Description: <br>
Git commit message expert. Analyzes diffs to generate perfect conventional commits, changelogs, release notes, and PR descriptions. Enforces commit message best practices and conventional commits spec. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryudi84](https://clawhub.ai/user/ryudi84) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to turn diffs, staged changes, commit lists, or branch summaries into conventional commit messages, changelogs, release notes, PR descriptions, version bump recommendations, and commit review feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated commit messages, changelogs, release notes, PR descriptions, or version bump recommendations may misclassify changes or omit important context. <br>
Mitigation: Review generated text against the actual diff, commit history, and release policy before committing, publishing, or merging. <br>
Risk: Diffs and commit histories may contain private keys, tokens, customer data, or sensitive internal URLs. <br>
Mitigation: Redact sensitive content before using the skill and avoid pasting secrets or confidential data into prompts. <br>


## Reference(s): <br>
- [Sovereign Commit Craft on ClawHub](https://clawhub.ai/ryudi84/sovereign-commit-craft) <br>
- [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) <br>
- [Keep a Changelog v1.1.0](https://keepachangelog.com/en/1.1.0/) <br>
- [Semantic Versioning v2.0.0](https://semver.org/spec/v2.0.0.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with commit-message, changelog, release-note, pull-request, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated text should be reviewed before use, especially when based on private diffs or commit history.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
