## Description: <br>
Installs ClawHub skills into a staging area, runs static security checks, and promotes or quarantines them based on scan results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to stage ClawHub skill installations, run automated static checks, and decide whether to promote or quarantine a skill after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shell script can promote or replace active OpenClaw skills. <br>
Mitigation: Use tightly scoped staging and live directories, keep backups of existing skills, and manually review staged files before promotion. <br>
Risk: The --force option can bypass VirusTotal flags from ClawHub. <br>
Mitigation: Avoid --force unless the specific scanner result has been reviewed and accepted. <br>
Risk: Automated static checks are a triage aid rather than a complete supply-chain security barrier. <br>
Mitigation: Run manual or deeper security review for WARN or FAIL results before promoting a quarantined skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zurbrick/skill-sandbox) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and terminal-oriented status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PASS, WARN, or FAIL verdicts and may move staged skill files into live or quarantine directories when its shell script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
