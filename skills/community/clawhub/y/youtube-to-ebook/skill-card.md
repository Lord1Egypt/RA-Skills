## Description:

Transform YouTube videos into beautifully formatted ebook articles with transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cclam5](https://clawhub.ai/user/cclam5)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, researchers, and individual readers use this skill to fetch recent long-form YouTube videos from selected channels, extract transcripts, turn them into readable articles, and package the results as an EPUB digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored API keys and optional Gmail app passwords can expose external service credentials if local configuration or logs are shared.

Mitigation: Keep .env private, use least-privileged keys or app passwords, rotate credentials after testing, and run the skill in an isolated environment.

Risk: Optional local scheduling can run the pipeline automatically with network and email access.

Mitigation: Review or disable scheduled automation and confirm project paths, recipients, and logging before enabling recurring runs.

Risk: Generated articles and emailed HTML or EPUB output may contain transcript errors or model-generated inaccuracies.

Mitigation: Inspect generated newsletters before relying on them or sharing them with others.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cclam5/skills/youtube-to-ebook)
- [Publisher profile](https://clawhub.ai/user/cclam5)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Anthropic Console](https://console.anthropic.com/)
- [Supadata transcript endpoint](https://api.supadata.ai/v1/transcript)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands; generated content may include Markdown articles, HTML newsletters, and EPUB files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided API keys for YouTube, Supadata, and Anthropic; optional Gmail credentials enable email delivery.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
