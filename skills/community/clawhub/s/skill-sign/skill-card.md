## Description: <br>
Cryptographically signs and verifies AgentSkill directories with Ed25519 so publishers can attach signatures and recipients can verify integrity and trusted authorship. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to generate local signing keys, sign skill directories, export public keys, and verify signed releases before trusting or distributing them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/songhonglei/skill-sign) <br>
- [RFC 8032: Edwards-Curve Digital Signature Algorithm](https://www.rfc-editor.org/rfc/rfc8032.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, terminal output, local key files, and sign.key JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Protect the local private key, use trusted out-of-band public keys for author verification, and use --force only when intentionally replacing a signing identity.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md Version field) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
