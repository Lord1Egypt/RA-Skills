## Description: <br>
Automates installation and configuration of TDengine 3.3.6.0, including download, installation, service startup, and basic database verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnnyhou327](https://clawhub.ai/user/johnnyhou327) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy a TDengine time-series database on Linux and verify that the service can list databases from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent database-service changes on the target machine. <br>
Mitigation: Review the exact commands, confirm the target host, and avoid running on production unless intended. <br>
Risk: A database service deployment can affect real data or credentials. <br>
Mitigation: Use least-privilege credentials, maintain backups for real data, and know how to stop, disable, and uninstall the service before installation. <br>


## Reference(s): <br>
- [TDengine 3.3.6.0 Linux x64 server package](https://www.taosdata.com/assets-download/TDengine-server-3.3.6.0-Linux-x64.tar.gz) <br>
- [ClawHub release page](https://clawhub.ai/johnnyhou327/tdengine-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Linux command-line tools: taos, systemctl, wget, and tar.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
