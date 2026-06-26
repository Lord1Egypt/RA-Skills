## Description: <br>
Seekdb routes agents to focused OceanBase SeekDB install, deploy, and source-build workflows for local server, embedded Python, and package build scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oceanbase](https://clawhub.ai/user/oceanbase) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to select and run the right SeekDB workflow for installing a local instance, using pyseekdb, or building binaries and packages across supported platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privileged install, service enablement, firewall, cleanup, or uninstall commands can change host state or remove SeekDB data. <br>
Mitigation: Review each command before execution, confirm before enabling persistent services or opening ports, and back up SeekDB data before cleanup or uninstall steps. <br>
Risk: Package installation instructions can depend on external mirrors, unsigned repository configuration, or downloaded installers. <br>
Mitigation: Prefer signed HTTPS package sources, avoid apt trusted=yes repository configuration where possible, and verify download sources before installing. <br>


## Reference(s): <br>
- [SeekDB product documentation](https://www.oceanbase.ai/docs/seekdb-overview/) <br>
- [SeekDB software download center](https://mirrors.oceanbase.com/oceanbase/community/stable/) <br>
- [Deploy SeekDB by systemd](https://docs.seekdb.ai/seekdb/deploy-by-systemd/) <br>
- [pyseekdb embedded install](https://docs.seekdb.ai/seekdb/pyseekdb-sdk-get-started/#install-pyseekdb) <br>
- [SeekDB Docker image documentation](https://github.com/oceanbase/docker-images/blob/main/seekdb/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/oceanbase/seekdb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes to install and build sub-skills; commands may require sudo, package managers, Docker, systemd, Android tooling, or Windows PowerShell depending on the chosen workflow.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
