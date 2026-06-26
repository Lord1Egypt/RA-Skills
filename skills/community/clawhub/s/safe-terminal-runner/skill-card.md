## Description: <br>
Forces the AI to use a "temporary file + environment variable isolation" workflow for script execution, completely resolving terminal freezes and escaping errors in Windows PowerShell/Bash. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zaynzhu](https://clawhub.ai/user/zaynzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run complex one-off scripts through temporary files instead of fragile inline terminal commands. It is intended for script execution tasks involving quoting, environment variables, SQL, JSON parsing, or regular expressions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temporary scripts can expose secrets or remain in the workspace after execution. <br>
Mitigation: Review each temporary script before running it, load secrets only when needed, keep temp_* ignored by version control, and delete temporary files after confirming the result. <br>
Risk: Standalone script execution can still run incorrect or unsafe logic if the generated script is not reviewed. <br>
Mitigation: Review the script contents and expected side effects before execution, especially for database, file system, API, or migration tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zaynzhu/safe-terminal-runner) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zaynzhu) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with code blocks and terminal commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces temporary-script execution guidance; temporary files should use a temp_ prefix and be cleaned up after execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
