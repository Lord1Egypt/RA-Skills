## Description:

Automates Twitter/X web posting through browser tools, including trend review, post drafting, and publishing with either automatic or manual confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:


## Use Case:

External users and social media operators use this skill to have an agent draft and publish posts from a logged-in Twitter/X web session. It is intended for browser-based posting workflows where the user may choose either review-first operation or fully automatic publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish generated public posts from a logged-in Twitter/X account without per-post confirmation.

Mitigation: Use review-first mode for normal use and reserve fully automatic posting for cases where the user explicitly accepts unattended public publishing.

Risk: Automated posting can trigger platform abuse or rate-limit controls if used repeatedly in a short period.

Mitigation: Limit posting frequency, avoid bulk rapid publishing, and stop after a small number of failed retries.

Risk: Generated social posts may contain unsafe, unlawful, hateful, violent, or otherwise inappropriate content.

Mitigation: Review generated content before posting and refuse or revise unsafe requests before using the browser publishing flow.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown or plain text with browser action guidance and posting status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the selected topic, final post text, success or failure status, failure reason, and resulting post URL.]

## Skill Version(s):

0.1.0 (source: release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
