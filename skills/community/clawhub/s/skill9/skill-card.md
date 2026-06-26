## Description: <br>
Cloud-synced skill vault - backup, version, and sync your AI agent skills across machines and platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shonge](https://clawhub.ai/user/shonge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install, configure, back up, sync, version, migrate, and uninstall AI agent skills across supported tools and machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sync local skill files to skill9's cloud service, which may expose secrets, proprietary content, or sensitive skill logic. <br>
Mitigation: Review local skills before syncing, remove secrets or proprietary content, and use the cloud sync only when the user accepts that data transfer. <br>
Risk: Setup and automation instructions can add ongoing sync behavior through agent rules or editor hooks. <br>
Mitigation: Inspect configured AGENTS.md rules and Claude or Cursor hooks, and disable automatic syncing when continuous backup is not desired. <br>
Risk: Installation depends on an npm package and GitHub login flow whose scopes and package integrity are outside the artifact. <br>
Mitigation: Verify the npm package source and requested GitHub permissions before login or installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shonge/skill9) <br>
- [skill9 setup guide](https://skill9.ai/SETUP.md) <br>
- [skill9 uninstall guide](https://skill9.ai/UNINSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands support --json and --platform options where documented.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
