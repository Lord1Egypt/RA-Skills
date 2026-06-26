## Description: <br>
Perform AMD SEV-SNP remote attestation to cryptographically verify VM identity and integrity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinyuwang](https://clawhub.ai/user/xinyuwang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to check SEV-SNP availability, generate attestation reports, fetch AMD certificates, and verify report signatures before trusting a VM with sensitive workloads or secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to /dev/sev-guest and may need root or sev-group permissions. <br>
Mitigation: Run it only on VMs you control, grant the minimum required device permissions, and review commands before using elevated privileges. <br>
Risk: Certificate retrieval depends on outbound HTTPS requests to AMD KDS. <br>
Mitigation: Allow only the expected AMD KDS endpoint and verify the ARK, ASK, and VCEK chain before relying on an attestation result. <br>
Risk: A valid report signature alone is not enough to decide whether a VM should receive secrets. <br>
Mitigation: Separately check REPORT_DATA or nonce freshness, the expected VM measurement, debug policy, and acceptable TCB levels. <br>
Risk: The workflow depends on third-party tools such as snpguest, OpenSSL, curl, and Rust tooling for installation. <br>
Mitigation: Install dependencies from trusted sources, pin or review versions where practical, and run the workflow in an environment appropriate for attestation testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xinyuwang/sev-attestation) <br>
- [Report fields](references/report-fields.md) <br>
- [Error codes and troubleshooting](references/error-codes.md) <br>
- [Manual verification](references/manual-verification.md) <br>
- [snpguest](https://github.com/virtee/snpguest) <br>
- [AMD KDS](https://kdsintf.amd.com) <br>
- [AMD SEV-SNP ABI Specification](https://www.amd.com/system/files/TechDocs/56860.pdf) <br>
- [AMD SEV documentation](https://developer.amd.com/sev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts can produce local attestation artifacts such as report.bin, nonce.hex, and AMD certificate files when run by the user.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
