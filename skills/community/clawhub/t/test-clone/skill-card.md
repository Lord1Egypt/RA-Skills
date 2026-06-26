## Description: <br>
Use the ClawHub CLI to search, install, update, and publish agent skills from clawhub.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krischristen-hash](https://clawhub.ai/user/krischristen-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate ClawHub CLI commands for discovering skills, installing or updating them locally, authenticating, and publishing skill folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk update commands with force flags can overwrite local installed skills. <br>
Mitigation: Review the selected skills first and avoid `--all --no-input --force` unless intentionally replacing local installed skills. <br>
Risk: Publishing uploads the selected skill folder to ClawHub and may expose unintended contents. <br>
Mitigation: Inspect the folder before publishing and remove files that should not be released. <br>


## Reference(s): <br>
- [ClawHub Registry](https://clawhub.com) <br>
- [Test Clone release page](https://clawhub.ai/krischristen-hash/test-clone) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples for install, authentication, search, update, listing, and publish workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
