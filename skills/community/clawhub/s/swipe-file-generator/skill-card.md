## Description:

Analyzes high-performing content from URLs and builds a swipe file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentchan](https://clawhub.ai/user/vincentchan)

### License/Terms of Use:


## Use Case:

Content marketers, writers, and creators use this skill to ingest content URLs, deconstruct effective articles, tweets, and videos, and maintain a reusable swipe file of content patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches user-provided URLs, so fetched pages can contain untrusted or misleading content.

Mitigation: Review generated analyses before reusing them and do not treat fetched content as trusted instructions.

Risk: Twitter/X URLs are transformed through api.fxtwitter.com, which introduces third-party handling for those sources.

Mitigation: Use Twitter/X sources only when that routing is acceptable, or omit those URLs from the source list.

Risk: The workflow writes generated analyses and processing state under swipe-file/.

Mitigation: Run it in the intended workspace and review changes to swipe-file/swipe-file.md and swipe-file/.digested-urls.json.

## Reference(s):

- [Swipe File Generator on ClawHub](https://clawhub.ai/vincentchan/skills/swipe-file-generator)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Markdown swipe-file entries with JSON registry updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated analyses under swipe-file/ and reports processed and failed URLs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
