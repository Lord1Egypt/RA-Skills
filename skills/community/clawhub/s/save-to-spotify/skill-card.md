## Description:

Create polished audio content and save to Spotify. Produces episodes with TTS narration, a rich timeline (chapters plus in-player images, external links, and Spotify entity cards), and a cover image. Also use for raw media saves, show/episode management, and timeline navigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spotify](https://clawhub.ai/user/spotify)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn authorized or user-provided material into narrated audio episodes, then save them to Spotify with cover artwork, chapters, and playback companions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect connected work accounts and send derived content to cloud services without clearly establishing those boundaries first.

Mitigation: Specify which calendars, repositories, and task accounts may be read; confirm which speech and image providers may receive content; prohibit confidential uploads; use a verified, versioned CLI and review installer side effects.

## Reference(s):

- [CLI usage](references/cli-usage.md)
- [Spotify API reference](references/spotify-api.md)
- [Audio providers and assembly](references/audio-providers.md)
- [Timeline format](references/timeline.md)
- [Cover images](references/cover-image.md)
- [Episode descriptions](references/episode-description.md)
- [Content quality](references/content-quality.md)
- [Onboarding](references/onboarding.md)
- [Local preview](references/local-preview.md)
- [Recipes](references/recipes.md)
- [Spotify Web API documentation](https://developer.spotify.com/documentation/web-api/tutorials/building-with-ai)
- [Spotify Web API OpenAPI schema](https://developer.spotify.com/reference/web-api/open-api-schema.yaml)
- [Spotify CLI releases](https://github.com/spotify/save-to-spotify/releases)

## Skill Output:

**Output Type(s):** [Audio files, Images, JSON, HTML, Text]

**Output Format:** [Narrated audio (MP3 by default), cover image, JSON timeline, and HTML episode description]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The resulting episode is saved privately to the user's Spotify library by default.]

## Skill Version(s):

0.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
