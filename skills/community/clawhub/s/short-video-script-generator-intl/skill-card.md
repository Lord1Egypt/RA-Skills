## Description:

Generates short-video scripts for TikTok, YouTube Shorts, Instagram Reels, Facebook Reels, and Snapchat with hooks, shot lists, voiceover, subtitles, background music suggestions, and calls to action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baolige2023](https://clawhub.ai/user/baolige2023)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and social media teams use this skill to draft platform-specific short-video scripts from a topic and selected duration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded service credentials can expose payment or AI service access.

Mitigation: Remove hardcoded keys, rotate exposed credentials, and load secrets from a managed runtime secret store before installation.

Risk: Debug server settings and all-interface binding can expose the app in deployment.

Mitigation: Disable debug mode and deploy behind an approved production server with restricted network binding.

Risk: Billing consent and pricing are inconsistent between the release description and application behavior.

Mitigation: Align all displayed prices, charge amounts, payment prompts, and consent flow before commercial use.

Risk: Payment redirects may send users to unvalidated URLs.

Mitigation: Validate payment URLs against the expected payment provider before redirecting users.

Risk: User prompts and generated scripts may be shared with a third-party AI service without clear disclosure.

Mitigation: Document third-party AI data sharing and avoid sensitive or regulated content until the data handling terms are reviewed.

Risk: Generated content rendered in the browser can create injection risk if not escaped.

Mitigation: Escape or sanitize generated fields before rendering or exporting user-visible content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baolige2023/skills/short-video-script-generator-intl)
- [Publisher profile](https://clawhub.ai/user/baolige2023)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured script text exportable as Markdown or TXT]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes hook, time-coded shots, voiceover, subtitles, background music suggestion, and CTA.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
