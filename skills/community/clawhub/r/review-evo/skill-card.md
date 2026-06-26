## Description: <br>
Self-improving code reviewer that learns your codebase over time. Analyzes git history, spots patterns, identifies risk, and gets smarter every run. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[8co](https://clawhub.ai/user/8co) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use ReviewEvo to review repository health, branch diffs, working changes, or targeted files using git history, code structure, and prior local review notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads repository code and git history to build review context. <br>
Mitigation: Install it only for repositories where this local analysis access is acceptable. <br>
Risk: The skill may create or append .review-evo/learnings.md with project patterns and review findings. <br>
Mitigation: Inspect the learning file before committing and add .review-evo/ to .gitignore when those notes should remain local. <br>
Risk: Branch review commands use user-provided branch names. <br>
Mitigation: Provide normal branch names and avoid shell-like input. <br>


## Reference(s): <br>
- [ReviewEvo ClawHub listing](https://clawhub.ai/8co/review-evo) <br>
- [ReviewEvo project homepage](https://github.com/8co/review-evo) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review report with findings, recommendations, and optional local learning notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append persistent review learnings to .review-evo/learnings.md in the target repository.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
