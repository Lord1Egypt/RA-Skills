## Description: <br>
Detect hardcoded secrets, exposed API keys, and credential misconfigurations in IaC and config files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to review redacted IaC, configuration, and exported AWS metadata for likely credential exposure, then plan migration to AWS Secrets Manager or Parameter Store. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A sample Lambda query can expose environment variable values even though the skill asks for names only. <br>
Mitigation: Review before installing, use only redacted files and outputs, avoid pasting raw Lambda configuration or environment variable values, and change the Lambda query to return variable names only. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/anmolnagpal/secrets-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with findings tables and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [References secret values by location only and does not output raw credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
