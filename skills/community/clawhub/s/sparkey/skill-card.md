## Description: <br>
Provides time-limited, self-revoking SSH access for AI agents using certificate TTL, user expiry, forced command restrictions, and scheduled automated cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanjeevneo](https://clawhub.ai/user/sanjeevneo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and support engineers use Sparkey to give an AI agent temporary, auditable SSH access for diagnosing or remediating Linux hosts. It is best suited for controlled support sessions where the operator can review privileged shell administration steps before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privileged SSH administration can change accounts, SSH configuration, timers, and local files on the operator or target host. <br>
Mitigation: Review the scripts before use, run grant-access.sh with --dry-run first, and execute only against the intended host from a controlled operator account. <br>
Risk: The CA private key is a persistent credential that can authorize future sessions if compromised. <br>
Mitigation: Keep the CA key on a hardened operator host, restrict it to root-only access, rotate it on a schedule, and consider offline or HSM-backed storage for high-security environments. <br>
Risk: Broader access profiles such as full or PTY mode can bypass the intended command restrictions. <br>
Mitigation: Prefer diagnostic mode with an agent-provided public key and escalate to remediation, full, or PTY only after explicit operator review. <br>
Risk: Cleanup can fail if at or systemd-run is unavailable or if sessions are interrupted. <br>
Mitigation: Confirm cleanup scheduling during grant, then run audit.sh and revoke-access.sh after each session to find and remove orphaned accounts, keys, shells, and timers. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/sanjeevneo/sparkey) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [License](LICENSE.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run privileged Linux SSH administration scripts; dry-run and diagnostic modes are documented.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
