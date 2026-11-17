## Description:

Intelligently compresses CLI output by removing comments, blank lines, and redundant content to reduce token use while preserving key information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efficiency97](https://clawhub.ai/user/efficiency97)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to compress large command outputs, file contents, test logs, JSON, and general text before passing them into an agent context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install and run an external PyPI package.

Mitigation: Use a virtual environment, avoid sudo or admin installation, and pin or verify the package version in sensitive workflows.

Risk: Artifact documentation uses both rtk-compressor and rtk-compress command names.

Mitigation: Confirm the installed command name before adopting the workflow in scripts or agent instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/efficiency97/skills/rtk-compressor)
- [Publisher Profile](https://clawhub.ai/user/efficiency97)
- [PyPI Package](https://pypi.org/project/rtk-compressor/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline shell and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reduce large command outputs by 60-90% depending on input type.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
