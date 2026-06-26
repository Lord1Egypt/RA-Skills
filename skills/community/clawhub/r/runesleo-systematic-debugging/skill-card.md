## Description: <br>
Four-phase debugging framework that ensures root cause investigation before attempting fixes. Never jump to solutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runesleo](https://clawhub.ai/user/runesleo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to debug bugs, test failures, build failures, performance issues, and unexpected behavior by recalling context, investigating root cause, comparing patterns, testing hypotheses, and implementing a single verified fix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic logging or investigation commands may expose secrets or personal data from the target repository or runtime. <br>
Mitigation: Review proposed logging and commands before running them, avoid collecting secrets or personal data, and keep diagnostics scoped to the intended repository. <br>
Risk: Remembered context or prior fixes may be stale, partial, or misleading for the current issue. <br>
Mitigation: Treat recalled context as a clue, then verify the current root cause with reproducible evidence before implementing a fix. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runesleo/runesleo-systematic-debugging) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code] <br>
**Output Format:** [Markdown with diagnostic notes, hypotheses, command snippets, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository-specific diagnostics, tests, or code changes when used by an agent.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
