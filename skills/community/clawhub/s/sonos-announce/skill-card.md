## Description:

Play audio on Sonos with intelligent state restoration - pauses streaming, skips Line-In/TV/Bluetooth, resumes everything.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdianova](https://clawhub.ai/user/clawdianova)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to play local audio announcements or sound effects on Sonos speakers while attempting to restore prior playback state afterward.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose files if its local HTTP server serves a broad or sensitive media directory.

Mitigation: Use it only on a trusted local network and keep media_dir limited to a dedicated non-sensitive audio folder.

Risk: Unsafe shell and process controls may run or kill unintended local commands or processes if paths or ports are user-controlled.

Mitigation: Avoid user-controlled paths and ports, and prefer a hardened version that uses subprocess without shell=True and targets only the intended process.

Risk: An unauthenticated local HTTP server may remain running after announcement playback.

Mitigation: Bind explicitly to the intended local interface, stop the server after use, and ensure cleanup runs even if playback or restoration fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawdianova/skills/sonos-announce)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python and bash code blocks; runtime function returns a Python dictionary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, ffprobe, and the soco Python package; announcement execution returns coordinator count and saved playback states.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; artifact frontmatter states 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
