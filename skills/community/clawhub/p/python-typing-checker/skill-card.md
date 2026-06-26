## Description: <br>
Analyze Python type annotation coverage and quality across Python codebases, including mypy compliance, untyped functions, Protocol usage, Generic types, TypeVar constraints, and modern typing patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit Python repositories for type annotation coverage, mypy readiness, modern typing patterns, and risky escape hatches such as Any, cast(), and type: ignore. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill from too broad a directory can expose more local source code than intended to the agent's review. <br>
Mitigation: Run it from the specific Python project directory to be audited and review proposed shell commands before execution. <br>
Risk: The analysis relies on shell-search heuristics and may produce incomplete or misleading typing findings. <br>
Mitigation: Validate findings with a project type checker such as mypy or pyright and review recommendations before applying changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with shell command snippets, findings, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only repository inspection; commands search the current working directory and exclude common virtual environment and cache paths where specified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
