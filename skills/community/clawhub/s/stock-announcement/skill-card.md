## Description:

Daily stock portfolio analysis with Gmail report delivery and Sonos voice announcement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a configured portfolio workflow use this skill to generate a daily stock performance report, send it through Gmail, and announce a short summary on a Sonos speaker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial portfolio summaries may be sent through the configured Gmail account.

Mitigation: Use a trusted recipient address and confirm that email delivery is acceptable for the portfolio information being summarized.

Risk: Financial summaries may be spoken aloud on the configured Sonos speaker.

Mitigation: Limit speaker selection to locations where the summary can be heard only by intended listeners.

Risk: The workflow depends on a Gmail OAuth token file.

Mitigation: Protect the Gmail OAuth token file and restrict workspace access to trusted users.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces portfolio summaries that may be delivered as HTML email content and spoken audio through configured external services.]

## Skill Version(s):

99.99.99 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
