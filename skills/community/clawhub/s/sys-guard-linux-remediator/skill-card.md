## Description: <br>
Host-based Linux incident response and remediation skill focused on precise threat detection, forensic-safe data collection, firewall control (iptables/nftables), integrity validation, and controlled remediation while preserving system stability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiaraho](https://clawhub.ai/user/kiaraho) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security engineers, system administrators, and incident responders use this skill to inspect Linux hosts, collect evidence, contain suspicious activity, and apply controlled remediation while preserving system stability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Administrator-level incident response commands can modify firewall rules, services, processes, and forensic state. <br>
Mitigation: Review each command before execution, capture pre- and post-change state, prefer reversible changes, and back up firewall and service configuration first. <br>
Risk: Raw third-party GitHub downloads are unpinned and may change over time. <br>
Mitigation: Replace raw download steps with pinned versions, checksum verification, or internally vetted forensic tools. <br>
Risk: Host-modifying remediation can reduce forensic preservation during strict evidence handling. <br>
Mitigation: Avoid modifying steps when preservation is required, hash artifacts before containment, quarantine rather than delete where possible, and log timestamped actions. <br>


## Reference(s): <br>
- [Skill source](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/kiaraho/sys-guard-linux-remediator) <br>
- [Publisher profile](https://clawhub.ai/user/kiaraho) <br>
- [Didier Stevens Suite base64dump.py](https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/base64dump.py) <br>
- [Didier Stevens Suite re-search.py](https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/re-search.py) <br>
- [Didier Stevens Suite zipdump.py](https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/zipdump.py) <br>
- [Didier Stevens Suite 1768.py](https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/1768.py) <br>
- [Didier Stevens Suite pdf-parser.py](https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/pdf-parser.py) <br>
- [Didier Stevens Suite oledump.py](https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/oledump.py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Analysis] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes host inspection, evidence collection, containment, firewall handling, and remediation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
