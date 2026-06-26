## Description: <br>
Recommend videos with precision, not addiction. Use when a user asks what to watch, wants video recommendations, wants a curated watchlist, wants direct video links, or wants suggestions based on recent chat instead of generic platform algorithms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to get concise, context-aware video recommendations, curated watchlists, and direct video links for a mood, project, current topic, or recent conversation context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use recent conversation context and durable preferences to personalize recommendations, which can expose private interests or sensitive context in the recommendation process. <br>
Mitigation: Avoid sharing private details unless they should influence recommendations, and ask the skill to ignore prior context when neutral recommendations are desired. <br>
Risk: Direct video links can route users to third-party platforms whose content, availability, recommendations, and data practices are outside the skill's control. <br>
Mitigation: Review linked videos before relying on them, prefer official or high-signal sources, and avoid treating third-party platform behavior as part of the skill's assurance boundary. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/fischerlam/video-recommendation) <br>
- [Source Strategy](artifact/references/source-strategy.md) <br>
- [Personalization](artifact/references/personalization.md) <br>
- [Output Patterns](artifact/references/output-patterns.md) <br>
- [Scoring Rubric](artifact/references/scoring-rubric.md) <br>
- [Testing](artifact/references/testing.md) <br>
- [Examples](artifact/references/examples.md) <br>
- [Taste Profiles](artifact/references/taste-profiles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown lists with video titles, direct links, and concise rationale when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce links-only output, grouped recommendations, shortlists, or project-aligned watchlists depending on the user request.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
