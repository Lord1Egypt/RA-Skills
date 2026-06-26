## Description: <br>
Fix PowerShell file encoding corruption (backtick, dollar sign, Chinese char mangling) when writing Node.js files on Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremycooper2077](https://clawhub.ai/user/jeremycooper2077) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose PowerShell-induced corruption in JavaScript and Node.js files, then apply safer write or repair steps. It includes a local Node.js helper for encoding diagnostics and limited GBK corruption repair. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local helper runs checks against a user-provided file path and can overwrite the target file in --fix mode. <br>
Mitigation: Run it only on files you control, inspect the path before execution, review diagnostic output first, and use --fix only when the backup-and-rewrite behavior is acceptable. <br>
Risk: Automatic repair is limited; backtick loss and dollar expansion may require restoration from original source. <br>
Mitigation: Keep or verify source backups, review repaired files before relying on them, and use source control or a clean copy when the diagnostic reports non-auto-repairable corruption. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeremycooper2077/pwsh-encoding-fix) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and a Node.js helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper can diagnose files and, in fix mode, rewrite a target file while creating a .bak backup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
