## Description:

Searches Stremio Web for movies or series and casts selected streams to a Chromecast device using Playwright and CATT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pedro-valentim](https://clawhub.ai/user/pedro-valentim)

### License/Terms of Use:


## Use Case:

External users or developers use this skill to automate Stremio Web playback and cast requested movies or series to a named Chromecast device in a local setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill under-discloses a hard-coded external streaming endpoint.

Mitigation: Review before installing and replace the hard-coded streamingServer with a user-approved local endpoint.

Risk: The browser automation weakens Chromium security controls.

Mitigation: Use only in a contained environment and remove the Chromium security-disabling flags before broader use.

Risk: Full stream URLs may be exposed in logs.

Mitigation: Avoid logging full stream URLs.

## Reference(s):

- [Stremio Web](https://app.strem.io/shell-v4.4/?streamingServer=https%3A%2F%2F192-168-15-162.519b6502d940.stremio.rocks%3A12470#/)
- [ClawHub Skill Page](https://clawhub.ai/pedro-valentim/skills/stremio-cast)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Markdown guidance with command-line invocation details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a content query and an optional Chromecast device name.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
