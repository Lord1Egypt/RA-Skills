## Description:

Streaming Buddy is a personal streaming assistant that tracks viewing activity, learns taste preferences, and recommends movies or TV shows by service, mood, and history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[udiedrichsen](https://clawhub.ai/user/udiedrichsen)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to manage a local streaming profile, track watch progress, maintain a watchlist and history, and get personalized movie or TV recommendations using configured services, moods, ratings, and TMDB-backed availability data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a TMDB API key and personal viewing profile data in the workspace.

Mitigation: Use a private workspace, avoid sharing or committing memory/streaming-buddy/config.json, and rotate the TMDB key if it has already been exposed.

Risk: Viewing-related searches and recommendation requests are sent to TMDB-backed endpoints.

Mitigation: Use explicit /stream commands, set the intended region and language, and avoid sensitive viewing queries when third-party API disclosure is unacceptable.

Risk: Streaming availability can be stale or regionally inaccurate.

Mitigation: Treat availability as advisory and verify the title in the relevant streaming service before relying on it.

## Reference(s):

- [Streaming Buddy Skill Page](https://clawhub.ai/udiedrichsen/skills/streaming-buddy)
- [Streaming Services Reference](references/services.md)
- [TMDB API Reference](references/tmdb-api.md)
- [JustWatch Integration](references/justwatch.md)
- [TMDB API Key Settings](https://www.themoviedb.org/settings/api)
- [TMDB Signup](https://www.themoviedb.org/signup)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with JSON-backed command results and inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq, curl, and a TMDB API key; stores configuration, services, viewing history, watchlist, preferences, and cached API responses under memory/streaming-buddy/.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
