## Description:

Overview skill for OceanBase SeekDB that routes agents to install, deploy, and build workflows for standalone SeekDB and embedded pyseekdb use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oceanbase](https://clawhub.ai/user/oceanbase)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose and run the appropriate SeekDB installation, deployment, or source-build workflow across supported platforms. It helps agents produce commands, configuration steps, diagnostics, and follow-up guidance for local server, Docker, systemd, MSI, pip-embedded, and package-build scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some install paths perform privileged and persistent system changes, including service enablement and data-directory changes.

Mitigation: Review commands before execution, confirm with the user before enabling boot-time services or deleting data, and verify service status and connectivity after changes.

Risk: Package sources and installers may be unsafe when fetched without strong verification, including the APT trusted HTTP source, remote yum script path, Docker latest tag, and MSI download.

Mitigation: Prefer signed package repositories, pinned Docker digests bound to 127.0.0.1, and verified MSI hashes or signatures; avoid remote-script and trusted HTTP paths unless independently trusted and verified.

## Reference(s):

- [SeekDB overview documentation](https://www.oceanbase.ai/docs/seekdb-overview/)
- [OceanBase software download center](https://mirrors.oceanbase.com/oceanbase/community/stable/)
- [Deploy by systemd](https://docs.seekdb.ai/seekdb/deploy-by-systemd/)
- [pyseekdb embedded install](https://docs.seekdb.ai/seekdb/pyseekdb-sdk-get-started/#install-pyseekdb)
- [SeekDB Docker image README](https://github.com/oceanbase/docker-images/blob/main/seekdb/README.md)
- [Windows MSI download](https://mirrors.oceanbase.com/oceanbase/community/stable/windows/11/x86_64/seekdb-1.3.0.0-win64.msi)
- [Install SeekDB locally](install/SKILL.md)
- [Build SeekDB](build/SKILL.md)
- [Docker install reference](install/references/docker.md)
- [Linux apt install reference](install/references/linux-apt.md)
- [Linux yum install reference](install/references/linux-yum.md)
- [Windows MSI install reference](install/references/windows-msi.md)
- [macOS Homebrew install reference](install/references/macos-homebrew.md)
- [Linux build reference](build/references/build-linux.md)
- [macOS build reference](build/references/build-macos.md)
- [Android build reference](build/references/build-android.md)
- [Windows build reference](build/references/build-windows.md)
- [Python wheel build reference](build/references/build-python-wheel.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell, PowerShell, batch, Python, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific command sequences, verification checks, service-management commands, and artifact paths.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
