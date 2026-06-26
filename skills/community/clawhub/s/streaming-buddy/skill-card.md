## Description: <br>
Streaming Buddy is a personal streaming assistant that tracks viewing activity, learns preferences from ratings and feedback, and recommends movies or TV shows by service, mood, and taste profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[udiedrichsen](https://clawhub.ai/user/udiedrichsen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to manage streaming services, track watch progress, maintain watchlists and history, and get personalized movie and TV recommendations using TMDB metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores streaming services, watch history, ratings, inferred preferences, cached TMDB responses, and the TMDB API key in the workspace. <br>
Mitigation: Install only if this local profile storage is acceptable, use a TMDB key intended for this skill, and delete $WORKSPACE/memory/streaming-buddy/ to reset the profile. <br>
Risk: The skill uses TMDB lookups for search, title details, watch-provider availability, and recommendations. <br>
Mitigation: Review the configured region, language, services, and TMDB key before use so recommendations and availability checks match the intended user context. <br>


## Reference(s): <br>
- [Streaming Buddy ClawHub Page](https://clawhub.ai/udiedrichsen/streaming-buddy) <br>
- [Publisher Profile](https://clawhub.ai/user/udiedrichsen) <br>
- [Streaming Services Reference](references/services.md) <br>
- [TMDB API Reference](references/tmdb-api.md) <br>
- [JustWatch Integration](references/justwatch.md) <br>
- [TMDB API Key Settings](https://www.themoviedb.org/settings/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON status and result objects, with agent-facing recommendation text or setup guidance derived from those results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local workspace state for services, watch history, ratings, inferred preferences, watchlists, and cached TMDB responses.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
