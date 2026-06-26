## Description: <br>
Validate, lint, diff, and inspect TOML configuration files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate TOML syntax, lint TOML configuration files, compare TOML configs, inspect structure, and extract keys from files such as pyproject.toml and Cargo.toml. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The show and diff commands may expose tokens, passwords, private endpoints, or other sensitive configuration values from TOML files in the agent conversation. <br>
Mitigation: Use the skill only on specific TOML files you intend to inspect, and avoid showing or diffing sensitive configuration files unless those values are safe to reveal. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown or text with inline shell commands and optional JSON or Markdown command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-specified TOML files and can display validation results, lint findings, parsed structure, extracted values, or diffs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
