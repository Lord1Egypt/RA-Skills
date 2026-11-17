## Description:

This skill guides an agent in using a local vRain installation to convert Markdown or plain-text Chinese classical texts into vertically typeset PDF ebooks in a traditional printed-book style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanleiguang](https://clawhub.ai/user/shanleiguang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare Chinese classical-text projects, configure vRain book assets, and run commands that generate vertically arranged classical-style PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to install and run unpinned third-party vRain and Perl dependencies.

Mitigation: Review before installing, use an isolated unprivileged environment, and pin or verify the vRain checkout and Perl dependency versions where possible.

Risk: The documented Perl dependency path includes an optional privileged `sudo cpan` install.

Mitigation: Prefer an unprivileged `cpanm` installation path and avoid privileged package installation unless a trusted administrator has reviewed it.

Risk: Rerunning generation commands may replace previously generated PDFs or images.

Mitigation: Confirm output paths before reruns and use the skill's test-page workflow before batch generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shanleiguang/skills/vrain)
- [ClawHub publisher profile](https://clawhub.ai/user/shanleiguang)
- [vRain upstream repository](https://github.com/shanleiguang/vRain)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent produces instructions and commands; generated PDFs and images are produced by the user's local vRain tools.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
