## Description:

Get Portland transit information including arrivals, trip planning, and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjrussell](https://clawhub.ai/user/mjrussell)

### License/Terms of Use:


## Use Case:

External users and transit-focused agents use this skill to answer questions about TriMet arrivals, trip planning, next departures, and service alerts in Portland, Oregon.

### Deployment Geography for Use:

Global, for Portland, Oregon transit information

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned global npm package.

Mitigation: Verify that trimet-cli is the intended package, consider pinning a reviewed version, and install it under a normal user account.

Risk: The skill requires a TRIMET_APP_ID environment variable.

Mitigation: Keep the API key scoped to TriMet API use and avoid exposing it in shared command output or logs.

## Reference(s):

- [ClawHub Trimet skill page](https://clawhub.ai/mjrussell/skills/trimet)
- [TriMet](https://trimet.org)
- [TriMet Developer API](https://developer.trimet.org/)
- [Publisher profile](https://clawhub.ai/user/mjrussell)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TriMet CLI commands that require the trimet binary and TRIMET_APP_ID environment variable.]

## Skill Version(s):

0.1.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
