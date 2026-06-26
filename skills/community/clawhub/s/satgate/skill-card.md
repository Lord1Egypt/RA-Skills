## Description: <br>
SatGate helps operators manage API gateway access, budgets, spending, token revocation, and gateway health from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matt-dean-git](https://clawhub.ai/user/matt-dean-git) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use SatGate to configure and operate SatGate CLI for API gateway access governance, including minting tokens, enforcing budgets, reviewing spend, and revoking compromised agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can fetch a remote SatGate binary, and the security summary notes that this release needs review because the binary source is not pinned. <br>
Mitigation: Prefer a pinned and checksum-verified release, build from source when appropriate, and use a user-owned install directory where possible. <br>
Risk: SatGate configuration can store powerful gateway or cloud tokens locally. <br>
Mitigation: Protect ~/.satgate/config.yaml as a secret, keep restrictive file permissions, and use least-privilege or short-lived tokens. <br>
Risk: SatGate commands can affect real gateway access, budgets, and token revocation. <br>
Mitigation: Run satgate status before changes, use --dry-run for destructive or high-budget operations, and avoid --yes without explicit approval. <br>


## Reference(s): <br>
- [SatGate homepage](https://satgate.io) <br>
- [ClawHub SatGate listing](https://clawhub.ai/matt-dean-git/satgate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some SatGate CLI commands can produce JSON when invoked with --json.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
