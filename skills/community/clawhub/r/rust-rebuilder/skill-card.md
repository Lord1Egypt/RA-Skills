## Description: <br>
Plan and execute incremental project rewrites to Rust with architecture mapping, parity verification, idiomatic Rust guidance, dependency preflight checks, and GitHub upstream synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dandandujie](https://clawhub.ai/user/dandandujie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan and carry out staged rewrites of existing projects into Rust while preserving behavior, validating parity, applying Rust design guardrails, and tracking upstream source changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends third-party helper skills or MCP repositories for search and GitHub workflows. <br>
Mitigation: Review the linked helper repositories independently before installation, as recommended by the security guidance. <br>
Risk: Bundled Python scripts can run local dependency checks and Git synchronization reports. <br>
Mitigation: Approve the bundled scripts before running them and only use Git sync reporting on repositories where fetching and pruning origin and upstream remotes is acceptable. <br>
Risk: Rewrite guidance can introduce behavior drift if migration batches are too broad or insufficiently tested. <br>
Mitigation: Use the skill's required staged migration contract, parity validation, risk register, and rollback notes for each batch. <br>


## Reference(s): <br>
- [rust-rebuilder ClawHub Page](https://clawhub.ai/dandandujie/rust-rebuilder) <br>
- [dandandujie Publisher Profile](https://clawhub.ai/user/dandandujie) <br>
- [Rust Backend Coding Guidelines](references/rust-backend-guidelines.md) <br>
- [GitHub Upstream Synchronization](references/github-upstream-sync.md) <br>
- [Rewrite Pitfalls and Antipatterns](references/rewrite-pitfalls-and-antipatterns.md) <br>
- [Rust Language Update Playbook](references/rust-language-update-playbook.md) <br>
- [grok-search Skill Repository](https://github.com/Frankieli123/grok-skill) <br>
- [grok-search MCP Repository](https://github.com/GuDaStudio/GrokSearch) <br>
- [github-helper Skill Repository](https://github.com/dandandujie/github-helper) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include rewrite scope, equivalence strategy, Rust design decisions, risk register, and upstream sync notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
