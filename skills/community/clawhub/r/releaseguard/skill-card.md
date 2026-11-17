## Description:

Scan, harden, sign, and verify release artifacts with ReleaseGuard — the artifact policy engine for dist/ and release/ outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asiridalugoda](https://clawhub.ai/user/asiridalugoda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to run ReleaseGuard on build outputs for release scanning, hardening, SBOM generation, signing, attestation, packaging, and verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alternate installation paths can run or install unverified remote code with broad local privileges.

Mitigation: Use trusted Homebrew installation or a pinned release with verified checksums or signatures; avoid curl | sh and unverified direct binary installation.

Risk: Signing, cloud obfuscation, and local-key workflows handle sensitive credentials or artifact integrity material.

Mitigation: Run these workflows only on intended artifact paths and provide OIDC tokens, private keys, or RELEASEGUARD_CLOUD_TOKEN only when the selected command requires them.

## Reference(s):

- [ReleaseGuard Repository](https://github.com/Helixar-AI/ReleaseGuard)
- [ClawHub Releaseguard Skill](https://clawhub.ai/asiridalugoda/skills/releaseguard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, configuration snippets, and references to optional CLI outputs such as JSON, SARIF, HTML, CycloneDX, SPDX, and VEX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the releaseguard binary. Some workflows require OIDC tokens, private signing keys, or RELEASEGUARD_CLOUD_TOKEN when explicitly selected.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
