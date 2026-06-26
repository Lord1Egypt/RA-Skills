## Description: <br>
Sign and verify agent skill folders with ed25519 keys. Detect tampering, manage trusted authors, and track provenance chains (isnād). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FELMONON](https://clawhub.ai/user/FELMONON) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to sign skill folders, verify file integrity, manage trusted signing keys, inspect signatures, and review provenance chains before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trusted-author checks, inspect output, and provenance chains can be misled by editable metadata, so they should not be treated as proof of author identity. <br>
Mitigation: Use this as a local utility until the trust-binding issue is fixed, verify public keys through independent channels, and review results before relying on them for security decisions. <br>
Risk: Local signing keys and trusted-key files affect whether signatures are accepted as trusted. <br>
Mitigation: Protect ~/.skillsign private keys, trust only keys from independently verified sources, and treat static or VirusTotal-clean results as supplemental rather than conclusive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FELMONON/skillsign) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create .skillsig manifests, signatures, signer metadata, provenance chains, and local key or trust files when commands are run.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
