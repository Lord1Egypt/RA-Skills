## Description: <br>
Scan, harden, sign, and verify release artifacts with ReleaseGuard, an artifact policy engine for dist/ and release/ outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asiridalugoda](https://clawhub.ai/user/asiridalugoda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to inspect, harden, package, sign, attest, and verify build outputs before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional curl-to-shell installer executes remote code. <br>
Mitigation: Prefer Homebrew or a pinned, verified release binary; review the installer source before running it in sensitive environments. <br>
Risk: Fix, harden, and obfuscate commands can mutate release artifacts. <br>
Mitigation: Run dry-run modes first, provide explicit artifact paths, and keep recoverable copies of release outputs. <br>
Risk: Signing, keyless signing, and cloud obfuscation may use private keys, OIDC tokens, or cloud tokens. <br>
Mitigation: Supply credentials only for commands that require them, keep local keys in controlled storage, and use CI secret handling for tokens. <br>
Risk: CVE enrichment, VEX generation, keyless signing, and higher obfuscation levels can contact external services. <br>
Mitigation: Use offline or local modes when external calls are not acceptable, and enable networked flags only after confirming policy approval. <br>


## Reference(s): <br>
- [ReleaseGuard ClawHub listing](https://clawhub.ai/asiridalugoda/releaseguard) <br>
- [ReleaseGuard GitHub repository](https://github.com/Helixar-AI/ReleaseGuard) <br>
- [ReleaseGuard install script source](https://github.com/Helixar-AI/ReleaseGuard/blob/main/scripts/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local artifact paths, optional output files, and release signing or cloud-service credentials only when the selected command requires them.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
