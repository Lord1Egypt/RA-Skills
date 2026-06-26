## Description: <br>
Deploy AI-generated static assets with StaticHub CLI using an explicit non-empty directory or `.html` file path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patrick0308](https://clawhub.ai/user/patrick0308) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to validate a static asset path, deploy it with the StaticHub CLI, and return the live URL and subdomain after a successful deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install the StaticHub CLI by piping an unverified remote shell script into `sh`. <br>
Mitigation: Review or replace the install step before use; prefer a trusted package manager or a pinned, verified release. <br>
Risk: Static-site deployment can publish local files to a public live URL. <br>
Mitigation: Deploy only files intentionally prepared for public access and validate the target path before running `statichub deploy`. <br>


## Reference(s): <br>
- [ClawHub Statichub skill page](https://clawhub.ai/patrick0308/statichub) <br>
- [StaticHub install script referenced by the skill](https://raw.githubusercontent.com/Patrick0308/statichub/main/scripts/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and deployment result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns repair commands when path validation fails; returns URL and subdomain on successful deployment.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
