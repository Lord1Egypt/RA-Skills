## Description: <br>
Runs local Ubuntu Pro, Livepatch, kernel, and module checks and can emit a JSON or Markdown security audit report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to inspect Ubuntu Pro and Livepatch status plus selected loaded kernel modules on an Ubuntu host. Treat it as a local audit helper, not as evidence of full CVE correlation, automated patch orchestration, or dashboarding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package description claims enterprise CVE correlation, real-time vulnerability prioritization, automated patch orchestration, and board-ready dashboards, but the artifact evidence supports only local Ubuntu status and module checks. <br>
Mitigation: Use it only as a local Ubuntu audit helper unless the publisher provides matching implementation evidence and clear documentation. <br>
Risk: The listing metadata includes unrelated financial referral promotion. <br>
Mitigation: Do not treat promotional links as part of the security workflow, and review the package carefully before installing. <br>
Risk: The security scanner verdict is suspicious even though the executable behavior appears mostly read-only. <br>
Mitigation: Inspect the installed files and run the skill in a least-privileged test environment before using results in compliance decisions. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/kingaiwork/ubuntu-pro-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/kingaiwork) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [JSON object, or JSON containing a Markdown report when report mode is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local command output from uname, Ubuntu Pro status, Canonical Livepatch status, and lsmod.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
