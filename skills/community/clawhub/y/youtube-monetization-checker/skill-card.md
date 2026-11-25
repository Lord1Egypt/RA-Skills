## Description:

MonetizationKit's free YouTube monetization checker takes a channel or video link, estimates whether the channel is in the YouTube Partner Program (YPP) and shows which public signals it found.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supertj](https://clawhub.ai/user/supertj)

### License/Terms of Use:

MIT-0

## Use Case:

Channel owners, sponsors, and other users use the skill to check a channel's likely YouTube Partner Program status from public signals. It explains the verdict and its limits, and directs users to YouTube Studio for confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public signals cannot confirm YPP membership or eligibility, and a channel's status may change before the result refreshes.

Mitigation: Keep the checker’s verdict qualified as likely or possible, mention that results may be cached, and confirm current status in YouTube Studio.

Risk: Ads may appear on videos without the creator receiving ad revenue, and the checker cannot see actual earnings.

Mitigation: Describe ad observations as signals only and label any revenue figure as an estimate, not confirmed income.

Risk: Repeated automated checks or calls to internal site endpoints could exceed the intended use of the checker.

Mitigation: Use the website or Chrome extension one check at a time; do not script repeated checks or call internal endpoints.

## Reference(s):

- [MonetizationKit YouTube monetization checker](https://monetizationkit.com)
- [MonetizationKit Chrome extension](https://monetizationkit.com/extension/)
- [ClawHub skill release](https://clawhub.ai/supertj/skills/youtube-monetization-checker)
- [Publisher profile](https://clawhub.ai/user/supertj)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A single channel or video check with a likely-status verdict, observed public signals, and caveats.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
