## Description: <br>
Set up IoT sensors and publish data to SKALE blockchain via SmartClaws. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dmytrotkk](https://clawhub.ai/user/dmytrotkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and IoT operators use this skill to install SmartClaws, initialize a wallet, register devices, and create sensor publisher scripts that publish readings to SKALE. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet setup and on-chain publishing can expose local wallet material or spend funded testnet assets. <br>
Mitigation: Use a minimally funded local wallet, keep ~/.smartclaws private, and avoid sharing command output that may expose sensitive wallet details. <br>
Risk: The skill installs a SmartClaws binary from a latest-release URL. <br>
Mitigation: Prefer a user-local install and pin and verify the downloaded binary when possible before running it. <br>
Risk: Generated publisher scripts and persistent services can publish incorrect readings or run with broad BLE privileges. <br>
Mitigation: Review generated scripts and service files before enabling them, confirm the exact sensor model and connection method, and avoid applying raw network capabilities to the system Python binary. <br>


## Reference(s): <br>
- [SmartClaws homepage](https://github.com/skalenetwork/smartclaws) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, Python, JSON, and systemd configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce hardware-specific publisher scripts and persistent service configuration after sensor details are confirmed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
