## Description:

Extracts video metadata from YouTube playlists using apidojo's YouTube Playlist Scraper on Apify for export or downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content curators, educators, and YouTube channel analysts use this skill to collect YouTube playlist video metadata for export, reporting, and downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Playlist URLs, search keywords, locale settings, and run parameters are sent to Apify/apidojo for processing.

Mitigation: Use the skill only when third-party processing is acceptable, and avoid private or sensitive playlist identifiers.

Risk: The optional customMapFunction input can run user-supplied JavaScript in the scraper workflow.

Mitigation: Use customMapFunction only when the supplied JavaScript is trusted and understood.

Risk: Very large playlists can create long-running jobs or excessive output.

Mitigation: Set maxItems to cap collection size when runtime or result volume matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-youtube-playlist)
- [Apify actor: apidojo/youtube-playlist-scraper](https://apify.com/apidojo/youtube-playlist-scraper)
- [Apify actor runs API endpoint](https://api.apify.com/v2/acts/apidojo~youtube-playlist-scraper/runs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell or API command examples and optional JSON or CSV result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces playlist video records including title, URL, description, duration, views, likes, availability status, channel details, keywords, live/private flags, and thumbnails.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
