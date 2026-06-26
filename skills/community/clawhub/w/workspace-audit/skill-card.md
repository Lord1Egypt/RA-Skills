## Description: <br>
Audits an OpenClaw workspace for stale paths, duplicate content, oversized files, possible secret leaks, and 1Password vault mismatches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheAgentWire](https://clawhub.ai/user/TheAgentWire) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace maintainers use this skill to run local OpenClaw workspace audits for structure, size limits, duplicate content, path references, credential-adjacent content, and optional 1Password vault alignment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit output may reveal sensitive file paths, credential-adjacent lines, or 1Password item names. <br>
Mitigation: Run the audit locally, avoid sharing full output, and redact sensitive names or paths before posting results. <br>
Risk: The optional 1Password check may scan more vault items than intended if no vault is selected. <br>
Mitigation: Set OP_VAULT to a specific trusted vault before running the 1Password audit. <br>
Risk: A local audit.conf file can alter size limits used by the structure audit. <br>
Mitigation: Keep audit.conf trusted and review custom limits before relying on audit results. <br>


## Reference(s): <br>
- [Workspace File Roles](references/file-roles.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/TheAgentWire/workspace-audit) <br>
- [TheAgentWire Publisher Profile](https://clawhub.ai/user/TheAgentWire) <br>
- [The Agent Wire](https://theagentwire.ai) <br>
- [1Password CLI Get Started](https://developer.1password.com/docs/cli/get-started/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, Configuration, Guidance] <br>
**Output Format:** [Terminal text and Markdown guidance with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit code 0 indicates all checks passed; exit code 1 indicates issues were found.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter states 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
