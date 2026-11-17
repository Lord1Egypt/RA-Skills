## Description:

Use the stravacli terminal tool to access Strava data (athlete profile, activities, streams, routes, segments, clubs, gear, uploads) and perform limited write actions (activity update/upload).

This skill is ready for commercial/non-commercial use.

## Publisher:

[brainsoft-raxat](https://clawhub.ai/user/brainsoft-raxat)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query Strava profile, activity, route, segment, club, gear, and upload data through stravacli, and to automate confirmed activity updates or uploads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned third-party stravacli executable that can access private fitness and location data.

Mitigation: Use a pinned reviewed release, verify checksums or signatures when available, and authenticate only after reviewing the requested Strava access.

Risk: The skill supports limited Strava write actions such as activity updates and uploads.

Mitigation: Require explicit user confirmation before write commands and review command arguments before execution.

## Reference(s):

- [stravacli source repository](https://github.com/Brainsoft-Raxat/strava-cli)
- [stravacli latest release](https://github.com/Brainsoft-Raxat/strava-cli/releases/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers --json for parseable Strava command results; write actions require user confirmation.]

## Skill Version(s):

2.2.98 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
