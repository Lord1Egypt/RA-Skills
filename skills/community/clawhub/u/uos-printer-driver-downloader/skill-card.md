## Description:

Searches the Tongxin UOS driver center for printer drivers and downloads matching .deb packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ykjack2005](https://clawhub.ai/user/ykjack2005)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support technicians use this skill to search UOS/Tongxin printer driver records, compare matching architectures, and download selected .deb packages for offline installation or workstation setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads driver packages from URLs returned by an external API, so an untrusted or compromised response could lead to unsafe packages.

Mitigation: Use the skill only for intended UOS printer-driver downloads and verify downloaded .deb packages through trusted vendor channels before installing them.

Risk: The skill writes files using metadata from API responses or the cached driver_list.json file.

Mitigation: Prefer a controlled output directory and inspect driver_list.json before using the two-step download flow.

Risk: The authoritative security verdict is suspicious because package downloads and file writes are not fully validated.

Mitigation: Review and scan the skill before deployment, and avoid installing any downloaded package until it has been independently checked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ykjack2005/skills/uos-printer-driver-downloader)
- [Tongxin UOS driver center](https://www.chinauos.com/resource/download-drivers)
- [UOS driver search API](https://www.chinauos.com/driver-api/v1/driver/query/list)
- [UOS driver download API](https://www.chinauos.com/driver-api/v1/driver/download?deb_id={deb_id}&driver_id={driver_id})

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown with inline shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads .deb packages to a dated printer_driver_YYYYMMDD directory and may write driver_list.json as a search cache.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
