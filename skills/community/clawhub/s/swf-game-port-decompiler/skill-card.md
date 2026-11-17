## Description:

Decompile SWF games for engine ports using FFDec/JPEXS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to extract SWF game code, assets, timeline renders, tag structure, XML data, and audit notes for migration into a modern engine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can overwrite or truncate writable output files when dump output is pointed at an existing file or unsafe path.

Mitigation: Review command arguments before running it, use a fresh output directory, and avoid using the source SWF or important project files as output paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stanestane/skills/swf-game-port-decompiler)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a decompile workspace with extracted code, assets, structure dumps, manifests, and porting audit notes when the helper script is run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
