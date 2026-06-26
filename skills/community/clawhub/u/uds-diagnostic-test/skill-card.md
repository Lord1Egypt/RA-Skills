## Description: <br>
Uds Diagnostic Test helps automotive engineers parse UDS diagnostic survey files, generate test scripts, run SocketCAN-based ECU tests, and produce reports and CAN logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tongli0406](https://clawhub.ai/user/tongli0406) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automotive diagnostic engineers use this skill for authorized bench or lab workflows that parse diagnostic survey inputs, confirm CAN and default-value assumptions, generate UDS test scripts, and review Markdown reports and CAN traces from ECU testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated UDS tests can change ECU state or host CAN settings. <br>
Mitigation: Use only on authorized bench or lab systems, review the generated test script before execution, and avoid running against live vehicles or shared workstations without review. <br>
Risk: Passwordless sudoers configuration for CAN setup can expand host-level risk. <br>
Mitigation: Avoid the passwordless sudoers rule unless the operator accepts the host risk; prefer reviewed, least-privilege setup on controlled machines. <br>
Risk: Pipeline mode can combine parsing, generation, and execution with fewer manual checks. <br>
Mitigation: Use the standard parse, confirm, generate, verify, and execute flow by default; reserve pipeline mode for explicit operator requests. <br>
Risk: SeedKey DLL loading can introduce untrusted executable logic. <br>
Mitigation: Load SeedKey DLLs only from trusted sources and review their use before SecurityAccess testing. <br>


## Reference(s): <br>
- [UDS NRC Reference](references/uds_nrc_reference.md) <br>
- [Linux CAN Project](https://github.com/linux-can) <br>
- [PEAK Linux Driver](https://github.com/linux-can/peak-linux-driver) <br>
- [Microsoft WSL USB Connection Guide](https://learn.microsoft.com/windows/wsl/connect-usb) <br>
- [usbipd-win WSL Support](https://github.com/dorssel/usbipd-win/wiki/WSL-support) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands plus generated Python scripts, JSON parser output, Markdown reports, and CAN log files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for authorized UDS diagnostic testing with SocketCAN-compatible hardware.] <br>

## Skill Version(s): <br>
2.9.1 (source: server release metadata; artifact frontmatter reports 2.9.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
