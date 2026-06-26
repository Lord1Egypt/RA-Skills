## Description: <br>
Automates Remnawave account administration, including setup, account creation, search, deletion, squad management, and account notification email workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uepuer](https://clawhub.ai/user/uepuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Administrators and operations engineers use this skill to manage Remnawave user accounts, synchronize internal squads, and send account provisioning emails from an agent-assisted command workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive VPN subscription URLs, Remnawave API tokens, SMTP credentials, and account logs may be exposed or persisted in local files. <br>
Mitigation: Use only in a controlled admin environment, rotate any exposed subscription URLs, keep generated .env/config/log files out of version control, and store credentials in a managed secret store. <br>
Risk: The release can be configured to bypass TLS certificate verification for Remnawave API or SMTP connections. <br>
Mitigation: Keep TLS verification enabled unless a managed internal trust setup explicitly requires otherwise. <br>
Risk: Hard-coded recipients, operational email addresses, and example subscription links can leak operational details if reused as-is. <br>
Mitigation: Redact package examples before sharing, replace hard-coded recipients with environment-specific configuration, and rotate any live links present in distributed artifacts. <br>


## Reference(s): <br>
- [Remnawave Robot ClawHub release page](https://clawhub.ai/uepuer/remnawave-robot) <br>
- [Publisher profile](https://clawhub.ai/user/uepuer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with Node.js command examples and generated configuration or log files when scripts are executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Remnawave and SMTP configuration, account creation logs, squad mappings, and notification email content.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
