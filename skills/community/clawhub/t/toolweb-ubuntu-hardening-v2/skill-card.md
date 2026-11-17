## Description:

Professional Ubuntu 22.04 LTS security configuration generator for STIG-compliant hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers, system administrators, and DevOps teams use this skill to generate Ubuntu 22.04 LTS hardening configuration files for selected kernel, SSH, firewall, audit, account, file-permission, network, and AppArmor controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests may include user identifiers when using the optional userId field.

Mitigation: Avoid sending real user identifiers unless they are needed for audit or operational tracking.

Risk: Generated hardening files can materially change Ubuntu host security behavior if applied without review.

Mitigation: Have an administrator review generated configurations and test them outside production before applying them to systems.

## Reference(s):

- [API Docs](https://api.mkkpro.com:8129/docs)
- [Ubuntu Hardening API Route](https://api.mkkpro.com/hardening/ubuntu-v2)

## Skill Output:

**Output Type(s):** [configuration, shell commands, text]

**Output Format:** [JSON containing generated hardening configuration data, file names, settings, command entries, descriptions, and a download URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns category-specific Ubuntu hardening configurations based on the requested hardening options.]

## Skill Version(s):

1.0.0 (source: release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
