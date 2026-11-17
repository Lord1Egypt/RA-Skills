## Description:

thoth-cli is a Hermetic divination CLI for astrology, tarot, gematria, and numerology that agents should run before interpreting positions, draws, or calculated values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aklo360](https://clawhub.ai/user/aklo360)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to install and operate the thoth CLI, then interpret CLI-produced astrology, tarot, gematria, and numerology results without fabricating calculated values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned global npm install can fetch a package version other than the reviewed release.

Mitigation: Verify the npm package and publisher before installation, pin the package version when possible, and avoid running global npm installs with administrator or root privileges.

Risk: Astrology positions, tarot draws, gematria values, or numerology calculations can be misleading if an agent fabricates them instead of using the CLI.

Mitigation: Run the thoth CLI first for positions, draws, and calculated values, then clearly separate CLI output from agent interpretation.

## Reference(s):

- [thoth-cli npm package](https://www.npmjs.com/package/thoth-cli)
- [thoth-cli full documentation](https://thothcli.com/skill.md)
- [thoth-cli website](https://thothcli.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI result interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide npm installation and thoth CLI execution; some CLI commands support JSON output.]

## Skill Version(s):

0.2.27 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
