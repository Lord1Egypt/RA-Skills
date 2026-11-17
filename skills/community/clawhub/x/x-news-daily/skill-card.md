## Description:

Fetches the top 10 X.com news items for a keyword, translates titles to Chinese, creates a full-screen poster, and sends it to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airbai](https://clawhub.ai/user/airbai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to request or schedule Chinese-language X.com news briefings for a chosen keyword. The skill gathers trending posts, summarizes and translates them, then prepares a poster-style file for delivery through a messaging channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill browses X.com and summarizes third-party social media content, which may be incomplete, misleading, or subject to access limits.

Mitigation: Use explicit keywords, review generated briefings before forwarding them, and treat the poster as a summary rather than a verified news report.

Risk: The skill creates local HTML/rendered artifacts and uses Chrome or screenshot tooling.

Mitigation: Run browser and screenshot commands in a trusted local environment and inspect generated files before sharing.

Risk: The skill can be used with scheduled tasks or third-party messaging delivery.

Mitigation: Confirm any schedule and destination channel before enabling recurring or external message delivery.

Risk: Generated posters include ClawHub/OpenClaw footer branding.

Mitigation: Make users aware of the footer before distributing generated artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/airbai/skills/x-news-daily)
- [Skill footer link](https://clawhub.ai/skill/x-news-daily)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML poster templates and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese summaries, local HTML or rendered poster artifacts, screenshots or PDFs, and messaging delivery guidance.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
