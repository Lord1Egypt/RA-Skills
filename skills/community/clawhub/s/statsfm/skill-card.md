## Description: <br>
Comprehensive music data tool for Spotify and Apple Music, powered by the stats.fm API, that can look up public album, artist, and chart data without an account and query personal listening history with a stats.fm username. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[space0mel](https://clawhub.ai/user/space0mel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query stats.fm music data, analyze personal Spotify listening history when a stats.fm username is supplied, and inspect public album, artist, track, and chart information without an account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query personal music-listening analytics from api.stats.fm when a username is provided. <br>
Mitigation: Provide usernames intentionally and ask the agent to limit queries when tighter privacy is desired. <br>
Risk: Deep analysis workflows can make repeated stats.fm API calls. <br>
Mitigation: Set clear bounds on date ranges, follow-up calls, and analysis depth when rate-control or data minimization matters. <br>


## Reference(s): <br>
- [stats.fm API Reference](references/api.md) <br>
- [stats.fm API Base URL](https://api.stats.fm/api/v1) <br>
- [statsfm-cli GitHub Repository](https://github.com/Beat-YT/statsfm-cli) <br>
- [Official stats.fm JavaScript Client](https://github.com/statsfm/statsfm.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with command examples and summarized music-listening analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stats.fm usernames, listening time ranges, artist or album identifiers, and public API query context.] <br>

## Skill Version(s): <br>
2.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
