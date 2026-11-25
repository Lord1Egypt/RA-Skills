## Description:

Create, query, modify, and delete Volcengine cloud resources with the `ve` CLI, including supported TOS, Ark, and TLS workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT

## Use Case:

Developers and cloud engineers use this skill to operate Volcengine resources, troubleshoot `ve` commands, and follow the supported workflows for TOS, Ark, and TLS tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was only partially complete and flagged unverified remote installer commands and API endpoint handling concerns.

Mitigation: Review the installer and API endpoint handling before installation; treat the scan as a review warning, not a finding of malicious intent.

## Reference(s):

- [Volcengine CLI releases](https://github.com/volcengine/volcengine-cli/releases)
- [Volcengine CLI installer](https://cloudcache.volccdn.com/ve/install.sh)
- [Ark CLI skills](https://github.com/volcengine/ark-cli/tree/main/skills)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands depend on the installed `ve` version, configured credentials, region, and applicable confirmation rules.]

## Skill Version(s):

1.1.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
