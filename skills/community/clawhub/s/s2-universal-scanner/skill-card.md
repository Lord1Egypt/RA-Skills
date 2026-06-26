## Description: <br>
Runs a consent-gated Python scanner that reports S2-native and legacy IoT sensor inventory for a target subnet. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and home or building automation operators can use this skill as a demonstration aid for S2-style sensor discovery workflows. Treat reported inventory as mock or unverified data until separately validated before onboarding devices or changing automations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner may present mock or unreliable sensor inventory as if it were real discovery data. <br>
Mitigation: Validate any reported devices with independent network or gateway tooling before using the inventory for decisions. <br>
Risk: Broad subnet scans or gateway tokens can expose network or home automation information. <br>
Mitigation: Limit scan scope, require explicit consent, and provide gateway credentials only when necessary. <br>
Risk: Agent examples could encourage onboarding devices or changing automation behavior from unverified output. <br>
Mitigation: Require separate human approval and validation before onboarding devices or modifying home or building automation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/spacesq/s2-universal-scanner) <br>
- [S2-SP-OS product page](https://space2.world/s2-sp-os) <br>
- [Space2 developer page](https://space2.world/developer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, S2_PRIVACY_CONSENT, and optionally S2_HA_TOKEN.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
