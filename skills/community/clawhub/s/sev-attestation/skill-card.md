## Description:

Perform AMD SEV-SNP remote attestation to cryptographically verify VM identity and integrity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinyuwang](https://clawhub.ai/user/xinyuwang)

### License/Terms of Use:


## Use Case:

Developers and infrastructure engineers use this skill to check SEV-SNP availability, generate attestation reports, fetch AMD certificates, and verify certificate chains and report signatures before relying on a confidential VM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can overstate what a PASS result proves before secrets are released.

Mitigation: Independently check nonce freshness, expected measurement, debug-bit state, and TCB policy before trusting the VM with secrets.

Risk: The scripts include privileged setup and device-access guidance.

Mitigation: Review commands before execution, avoid running the whole workflow as root where possible, and make persistent module or device-permission changes only with a rollback plan.

Risk: Dependency installation guidance can fetch mutable upstream code.

Mitigation: Prefer pinned and verified dependency installation instead of unversioned cargo installs or shell installers.

## Reference(s):

- [SEV-SNP Attestation Report Fields](references/report-fields.md)
- [SEV-SNP Attestation Error Codes and Troubleshooting](references/error-codes.md)
- [Manual SEV-SNP Verification with OpenSSL](references/manual-verification.md)
- [virtee/snpguest](https://github.com/virtee/snpguest)
- [AMD KDS](https://kdsintf.amd.com)
- [ClawHub skill page](https://clawhub.ai/xinyuwang/skills/sev-attestation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and generated attestation output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce report.bin, nonce.hex, request_data.bin, and certificate files when the shell scripts are executed.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
