## Description: <br>
Lint .sql migration files for common mistakes - missing IF EXISTS guards, UPDATE/DELETE without WHERE, non-idempotent CREATE, missing transaction wrappers, reserved-word identifiers, destructive DDL, and Postgres-specific issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to lint SQL migration files before review, pre-commit checks, or CI gates. It flags unsafe, non-idempotent, destructive, and dialect-specific migration patterns so teams can review them before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The linter can block CI or pre-commit workflows when warnings or errors meet the configured threshold. <br>
Mitigation: Choose severity thresholds deliberately and start with reporting-only or error-only gates before enforcing stricter warning gates. <br>
Risk: The tool reads user-selected SQL migration files and reports findings based on rule-based analysis without schema knowledge. <br>
Mitigation: Run it only on migration directories intended for inspection and review findings before changing or deploying migrations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Text, JSON, and summary reports from command-line linting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports severity filtering, dialect selection, recursive directory linting, and CI-friendly exit codes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
