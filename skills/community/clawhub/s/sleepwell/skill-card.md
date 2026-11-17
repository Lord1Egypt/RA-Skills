## Description:

Sleepwell is a wellness-branded logging skill for sleep and productivity entries, including bedtimes, schedules, streaks, reviews, statistics, search, and export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to log, review, search, and export sleep or productivity journal entries over time. Because the release security evidence flags broad persistent logging behavior, it should be used only for non-sensitive personal or work notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wellness branding may lead users to store sensitive health, credential, customer, incident, or confidential planning data in persistent local logs.

Mitigation: Treat the skill as a general journal and productivity logger; do not enter secrets, regulated health information, customer data, incident details, or confidential work plans.

Risk: The skill persistently stores, searches, and exports arbitrary entries from local files.

Mitigation: Use it only on trusted single-user systems, review exported files before sharing, and apply restrictive file permissions for the data directory.

Risk: The security evidence flags unsafe shell argument handling and file permission concerns.

Mitigation: Review and fix shell argument handling and file permissions before accepting untrusted inputs or running on shared systems.

## Reference(s):

- [Sleepwell ClawHub listing](https://clawhub.ai/ckchzh/skills/sleepwell)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local log and export files when installed and executed by the user.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
