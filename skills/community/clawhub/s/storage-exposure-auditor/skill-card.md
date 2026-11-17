## Description:

Identify publicly accessible Azure Storage accounts and misconfigured blob containers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers, cloud security teams, and Azure administrators use this skill to review exported Azure Storage account and blob container configuration for public exposure, missing hardening controls, and policy recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill recommends broad write-capable Azure permissions for a read-only workflow.

Mitigation: Use the narrowest read-only Azure roles and scopes available, such as Reader for account-level configuration and Storage Blob Data Reader for container listing, instead of Storage Account Contributor.

Risk: Exported Azure configuration can include sensitive account names, resource groups, network rules, tenant details, tokens, keys, or other identifiers.

Mitigation: Redact sensitive identifiers, tokens, keys, and tenant details before sharing exported data for analysis.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with findings tables, Azure CLI examples, ARM or Bicep snippets, and Azure Policy guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only analysis of user-provided exported configuration data; the skill does not require credentials or direct Azure access.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
