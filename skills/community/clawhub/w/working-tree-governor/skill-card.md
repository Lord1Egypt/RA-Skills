## Description: <br>
Govern dirty git working trees by classifying runtime noise vs real source changes, defaulting to selective staging, verifying staged scope, and asking the operator when scope is ambiguous. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lobsterquant](https://clawhub.ai/user/lobsterquant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when a repository has a noisy dirty working tree and they need guidance for classifying changes, staging only relevant source or test files, verifying staged scope, and deciding when operator approval is required before commit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ambiguous or large staged file sets can cause unrelated source files, runtime state, logs, caches, or generated outputs to be committed. <br>
Mitigation: Keep the approval gate for ambiguous or large staged sets and verify staged paths with cached diff commands before committing. <br>
Risk: Repository-specific path conventions can cause important local files to be misclassified as noise. <br>
Mitigation: Review and adapt the path-bucketing rules for each repository before relying on automatic include or exclude recommendations. <br>


## Reference(s): <br>
- [Working Tree Governor ClawHub Release](https://clawhub.ai/lobsterquant/working-tree-governor) <br>
- [lobsterquant Publisher Profile](https://clawhub.ai/user/lobsterquant) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown with inline shell commands and staged-scope recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dirty-tree summaries, bucket classifications, include and exclude recommendations, commit-message guidance, and operator approval questions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
