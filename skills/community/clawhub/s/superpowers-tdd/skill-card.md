## Description: <br>
Enforces a strict RED-GREEN-REFACTOR TDD cycle by requiring a failing real-code test before implementation, minimal code to pass it, and refactoring only after tests are green. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill before implementing a feature or bug fix to follow test-driven development: write a failing test, verify the failure, implement the minimum code, verify the pass, and then refactor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to run project test commands while developing. <br>
Mitigation: Run tests in an appropriate workspace or sandbox and review the selected commands before execution. <br>
Risk: Security guidance notes broad but visible execution options for review workflows. <br>
Mitigation: Use --dry-run first, disable yolo mode with --no-yolo or AUTOREVIEW_YOLO=0, and set --fallback-reviewer none when diffs should not be sent to other reviewer CLIs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/superpowers-tdd) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/axelhu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown process guidance with code examples, shell command examples, and completion checklists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to run project-appropriate tests and keep implementation limited to behavior covered by failing tests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
