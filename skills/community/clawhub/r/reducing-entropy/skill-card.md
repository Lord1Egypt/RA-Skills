## Description: <br>
Minimize total codebase size through ruthless simplification. Measure success by final code amount, not effort. Bias toward deletion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill during refactoring, feature work, code review, and tech-debt reduction to challenge unnecessary complexity and reduce the final size of the codebase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Simplification guidance may lead an agent to delete code, tests, abstractions, or files that still protect needed behavior. <br>
Mitigation: Use the skill on a branch, inspect all proposed removals, and run relevant tests before accepting deletions. <br>
Risk: The artifact contains no server-resolved import provenance for this release. <br>
Mitigation: Install only from a trusted source and prefer reviewed or pinned source when provenance matters. <br>


## Reference(s): <br>
- [Reducing Entropy on ClawHub](https://clawhub.ai/wpank/reducing-entropy) <br>
- [Simplicity vs Easy](references/simplicity-vs-easy.md) <br>
- [Composition Over Construction](references/design-is-taking-apart.md) <br>
- [Data-Oriented Design](references/data-over-abstractions.md) <br>
- [PAGNI: Probably Are Gonna Need It](references/expensive-to-add-later.md) <br>
- [Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/) <br>
- [The Grug Brained Developer](https://grugbrain.dev/) <br>
- [Out of the Tar Pit](https://curtclifton.net/papers/MosesleyMarks06a.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown guidance with checklists, review prompts, and code-change recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend deleting code, tests, abstractions, or files; proposed removals should be reviewed and tested.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
