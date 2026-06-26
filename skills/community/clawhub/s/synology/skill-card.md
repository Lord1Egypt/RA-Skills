## Description: <br>
Plan, harden, and recover Synology NAS and DSM setups with storage design, backup discipline, remote access, and Container Manager workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
NAS administrators, home-lab users, and small-business operators use this skill to plan DSM storage, backup, remote access, package, Container Manager, migration, and incident recovery work with explicit safety gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live NAS work can change storage, permissions, remote access, restores, or package state. <br>
Mitigation: Confirm the exact NAS, affected volume or package, backup freshness, rollback plan, and whether each step is read-only or mutating before making changes. <br>
Risk: Users may expose credentials, recovery secrets, serial numbers, or sensitive support data while troubleshooting. <br>
Mitigation: Do not paste DSM passwords, OTP codes, private keys, recovery secrets, serial numbers, or secret-bearing support bundles into chat or local notes. <br>
Risk: Remote access guidance can increase DSM, SSH, or package dashboard exposure if applied without guardrails. <br>
Mitigation: Prefer private access paths such as VPN or approved QuickConnect workflows, and require explicit approval, MFA, current updates, and rollback documentation before public exposure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/synology) <br>
- [Publisher Profile](https://clawhub.ai/user/ivangdavila) <br>
- [Skill Homepage](https://clawic.com/skills/synology) <br>
- [Synology Official Site](https://www.synology.com) <br>
- [Synology Knowledge Center](https://kb.synology.com) <br>
- [Backup and Recovery](backup-and-recovery.md) <br>
- [Storage and Shares](storage-and-shares.md) <br>
- [Remote Access and Networking](remote-access-and-networking.md) <br>
- [Packages and Containers](packages-and-containers.md) <br>
- [Troubleshooting](troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists, execution records, configuration notes, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update optional local notes under ~/synology/ only after user confirmation; does not require credentials for planning or review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
