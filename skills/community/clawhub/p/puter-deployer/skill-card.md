## Description: <br>
Deploy or update Puter-hosted web apps/sites with a CLI-first, verify-first workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[logclinker](https://clawhub.ai/user/logclinker) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to publish, update, verify, troubleshoot, and prepare rollback notes for Puter-hosted web apps or sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an authenticated Puter CLI session to update hosted apps or sites, including production targets. <br>
Mitigation: Confirm the account, target app or site, build output directory, production overwrite intent, expected URL, and rollback artifact before running deployment steps. <br>
Risk: Deployment can appear successful while serving the wrong content or failing at the final URL. <br>
Mitigation: Run the included URL verification step and require HTTP 200 plus the expected content marker when provided. <br>
Risk: Troubleshooting output could expose credentials or sensitive session details. <br>
Mitigation: Report status and failure category only, and do not print authentication tokens or secret values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/logclinker/puter-deployer) <br>
- [Puter API Fallback](references/api-fallback.md) <br>
- [Puter Deploy Checklist](references/deploy-checklist.md) <br>
- [Puter Deploy Failure Playbook](references/failure-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and deployment report fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes verification status, deployed URL, source commit, rollback artifact, and rollback command when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
