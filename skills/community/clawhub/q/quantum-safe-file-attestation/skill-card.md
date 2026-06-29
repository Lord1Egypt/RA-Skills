## Description: <br>
Quantum Safe File Attestation helps agents issue, verify, and inspect post-quantum file attestation packages for artifacts stored through AgentPMT tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, release engineers, and auditors use this skill to create attestation packages for files, verify packages against original artifacts, and retrieve public-key information for independent review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File identifiers, artifact names, and metadata may expose sensitive project or release information. <br>
Mitigation: Keep names and metadata non-sensitive, and avoid placing secrets or personal data in tool inputs. <br>
Risk: Cryptography and hardware-key claims may need independent review before use in compliance or release-signing workflows. <br>
Mitigation: Verify the vendor's cryptographic, hardware-key, and attestation claims before relying on the skill for regulated or high-assurance workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/quantum-safe-file-attestation) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/quantum-safe-file-attestation) <br>
- [Independent Offline Verifier](https://github.com/Abraxas1010/verified-pqc-verifier) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, guidance] <br>
**Output Format:** [Structured JSON responses with identifiers, hashes, verification status, and public-key details, plus concise usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions include attest_artifact, verify_attestation, and get_public_key; file IDs and optional metadata are used as inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
