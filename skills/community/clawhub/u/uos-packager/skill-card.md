## Description:

Packages application files into UOS/deepin-compliant Debian packages under /opt/apps/${appid}/ with required info, desktop, icon, build, and inspection helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaneniu](https://clawhub.ai/user/zaneniu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and packaging engineers use this skill to create, adapt, build, and inspect Debian packages that follow UOS/deepin application layout and metadata requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or adapted maintainer scripts may change privileged system files, including udev rules, before package installation.

Mitigation: Review maintainer scripts before installing packages with sudo; only use fixed, necessary, and reviewed destinations and contents.

Risk: Generic privileged-file-write examples can be unsafe if copied without validating the destination and input content.

Mitigation: Prefer package-managed system files, validate script inputs, and avoid following generic udev or privileged-write examples unless they are necessary and reviewed.

Risk: Temporary build directory handling may be unsuitable for shared or privileged build environments.

Mitigation: Harden temporary directory handling before using the helper scripts in shared or privileged environments.

## Reference(s):

- [UOS/deepin packaging guidance](artifact/SKILL.md)
- [UOS application scaffold template](artifact/references/template_build.sh)
- [Debian package build helper](artifact/scripts/build_deb.sh)
- [Debian package inspection helper](artifact/scripts/introspect.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, INI examples, and bash helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces packaging instructions and local helper commands; generated maintainer scripts and privileged installation steps require review before use.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
