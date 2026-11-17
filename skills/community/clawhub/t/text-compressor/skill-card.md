## Description:

Compress and decompress text files using smart abbreviation and whitespace normalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to shrink, clean up, or approximately restore text files while preserving basic readability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes unrelated packaging helpers, including one that can execute Python code from a hard-coded external OpenClaw workspace path.

Mitigation: Review before installing, trust the publisher before use, and remove or ignore the packaging helper scripts; use only the text compression script when compression is the intended task.

Risk: Higher compression levels and decompression are lossy or approximate.

Mitigation: Keep backups of source files and use level 1 when text fidelity matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/skills/text-compressor)
- [Publisher profile](https://clawhub.ai/user/fuzzyb33s)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Plain text files with terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compression levels 2 and 3 may reduce readability; decompression is approximate.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
