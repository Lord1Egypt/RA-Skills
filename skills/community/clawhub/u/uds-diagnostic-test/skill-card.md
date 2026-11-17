## Description:

UDS Diagnostic Test helps agents parse UDS diagnostic survey files, generate Python-based diagnostic test scripts, initialize SocketCAN, execute authorized ECU tests, and produce test reports and CAN trace logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tongli0406](https://clawhub.ai/user/tongli0406)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automotive test engineers use this skill to turn diagnostic survey data into UDS test scripts, validate CAN connectivity, and run ECU diagnostic tests on an authorized SocketCAN test bench.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make persistent privileged host changes, including CAN kernel module loading, CAN interface configuration, and optional sudoers changes.

Mitigation: Install and run it only on a dedicated, authorized ECU test bench or isolated lab machine, and do not apply the NOPASSWD sudoers rule on shared workstations.

Risk: Generated and executed UDS tests can change ECU state through reset, clear-DTC, write, SecurityAccess, memory, transfer, IOControl, RoutineControl, or ControlDTCSetting paths.

Mitigation: Review generated scripts before execution and require explicit approval for state-changing tests, especially before running against production vehicles or ECUs.

Risk: Missing or defaulted CAN parameters can cause tests to target the wrong bus configuration or produce misleading results.

Mitigation: Preserve the documented confirmation step for TX/RX CAN IDs, bitrate, CAN FD settings, defaults, and missing survey attributes before generating scripts with the confirmed flag.

## Reference(s):

- [UDS NRC Reference](references/uds_nrc_reference.md)
- [PEAK Linux Driver Repository](https://github.com/linux-can/peak-linux-driver)
- [Linux CAN Project](https://github.com/linux-can)
- [Microsoft WSL USB Connection Guide](https://learn.microsoft.com/windows/wsl/connect-usb)
- [usbipd-win WSL Support](https://github.com/dorssel/usbipd-win/wiki/WSL-support)
- [usbipd-win Troubleshooting](https://github.com/dorssel/usbipd-win/wiki/Troubleshooting)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated Python test scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce Markdown UDS test reports and ASC CAN trace logs when executed on authorized SocketCAN hardware.]

## Skill Version(s):

2.9.1 (source: server release evidence; artifact frontmatter and changelog list 2.9.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
