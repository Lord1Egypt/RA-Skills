## Description: <br>
Identify publicly accessible Azure Storage accounts and misconfigured blob containers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security engineers, cloud administrators, and developers use this skill to review exported Azure Storage account and blob container configuration for anonymous access, public network exposure, missing protection settings, and hardening recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The permission guidance may lead users to grant broader Azure access than needed for a manual storage exposure review. <br>
Mitigation: Use least-privilege read-only access, such as Reader for account configuration and Storage Blob Data Reader scoped only to required storage accounts or resource groups; provide redacted exported configuration only, never access keys, SAS secrets, tokens, or credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/anmolnagpal/storage-exposure-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with findings, tables, policy guidance, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided exported Azure configuration data and does not require direct Azure account access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
