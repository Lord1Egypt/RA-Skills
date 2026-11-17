## Description:

Transforms YouTube videos into Telegraph Instant View articles with visual slides and timestamped summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viticci](https://clawhub.ai/user/viticci)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to turn YouTube links into public Telegraph articles that combine a video link, extracted slides, timestamped summaries, and notable quotes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish YouTube-derived text and extracted frames to public or externally hosted services.

Mitigation: Use only videos that may be shared publicly, and avoid private, unlisted, sensitive, or embargoed videos unless external publication is acceptable.

Risk: The wrapper can load broad local credential files.

Mitigation: Provide only TELEGRAPH_TOKEN and OPENAI_API_KEY through a scoped environment or secret manager, and avoid broad .env sourcing.

Risk: Debug mode can retain local extracted media.

Mitigation: Run without --debug for routine use and remove temporary media when debugging is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viticci/skills/youtube-instant-article)
- [summarize CLI](https://github.com/steipete/summarize)
- [Telegraph API](https://telegra.ph/api)
- [catbox.moe](https://catbox.moe)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Markdown]

**Output Format:** [Command output with a Telegraph article URL and a public article containing timestamped text and embedded images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires zsh, summarize v0.10.0 or later, jq, curl, TELEGRAPH_TOKEN, and OPENAI_API_KEY; optional debug mode retains temporary slide files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
