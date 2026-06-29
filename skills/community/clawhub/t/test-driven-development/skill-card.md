## Description: <br>
Test-driven development for non-trivial behavior: write or update a failing test first, observe the expected failure, then implement the minimal code needed to pass while keeping the test suite aligned with the current target. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentjiang06](https://clawhub.ai/user/vincentjiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill when implementing real logic, fixing bugs, or changing tested behavior. It guides the agent to right-size TDD, prefer editing or merging existing tests over piling on duplicates, run targeted tests, and report concrete red/green evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to edit, merge, or delete tests while keeping the suite aligned with changed behavior. <br>
Mitigation: Review test deletions and consolidations in the resulting diff, and require the agent to report what was added, edited, merged, or deleted. <br>
Risk: The skill can direct targeted test runs and bug-fix verification steps that involve reverting or restoring implementation changes. <br>
Mitigation: Use repository-native targeted test commands, inspect command output and exit status, and review any checkpoint, revert, or restore operation before applying it in important repositories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vincentjiang06/skills/test-driven-development) <br>
- [Enforcement gates](references/enforcement-gates.md) <br>
- [Modify mode](references/modify-mode.md) <br>
- [Refactor and legacy code](references/refactor-and-legacy.md) <br>
- [Testing anti-patterns](references/testing-anti-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell command evidence, and concise change summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include targeted test output, exit status, and a summary of tests added, edited, merged, or deleted.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
