## Description:

ReSoul resets OpenClaw's persona and bootstrap state by fetching the official BOOTSTRAP.md after explicit second confirmation and archiving existing SOUL.md, USER.md, and IDENTITY.md files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tacitlab](https://clawhub.ai/user/tacitlab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use ReSoul when they need to reinitialize a workspace identity and restore the upstream bootstrap flow while preserving previous identity files in .trash/.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill replaces persistent OpenClaw bootstrap state with mutable network-fetched instructions.

Mitigation: Review or pin the downloaded BOOTSTRAP.md source before starting a new session with /new.

Risk: The skill moves SOUL.md, USER.md, and IDENTITY.md out of the workspace root after prose-only confirmation.

Mitigation: Confirm the exact workspace path and require explicit second confirmation before running the reset.

## Reference(s):

- [ClawHub ReSoul skill page](https://clawhub.ai/tacitlab/skills/resoul)
- [Official OpenClaw BOOTSTRAP.md template](https://raw.githubusercontent.com/openclaw/openclaw/main/docs/reference/templates/BOOTSTRAP.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file path summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit second confirmation before destructive file moves.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
