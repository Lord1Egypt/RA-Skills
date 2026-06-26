## Description: <br>
Comprehensive Elixir/Phoenix code review with optional parallel agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Elixir and Phoenix code changes, run expected Mix checks, load applicable review skills, and consolidate file-line findings into a single review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may run normal project development commands such as Mix formatting, Credo, Dialyzer, grep, git diff, and tests in the target repository. <br>
Mitigation: Use it in repositories where executing the project's normal development commands is acceptable, and review commands before running them in untrusted projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/review-elixir) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with issue sections and inline shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May dispatch specialized subagents when --parallel is supported; otherwise produces the same review structure sequentially.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
