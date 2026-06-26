## Description: <br>
Fetches NYC subway departure times for all subway lines using MTA realtime feeds with scheduled fallback for future times. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nyluke](https://clawhub.ai/user/nyluke) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and transit-focused agents use this skill to answer questions about NYC subway departures, commute timing, next trains, station matches, direction filters, and future scheduled service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts MTA data services to retrieve realtime and schedule data. <br>
Mitigation: Run it in an environment where outbound access to public MTA endpoints is permitted and expected. <br>
Risk: The skill stores downloaded schedule data in a local cache. <br>
Mitigation: Review local cache policy for the runtime environment and clear ~/.cache/subwayskill if cached transit data should not persist. <br>
Risk: Transit predictions and scheduled fallbacks can be stale, delayed, or unavailable depending on MTA feed status. <br>
Mitigation: Treat outputs as trip-planning guidance and verify time-sensitive travel decisions with an authoritative transit source when necessary. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nyluke/subwayskill) <br>
- [Publisher Profile](https://clawhub.ai/user/nyluke) <br>
- [SubwaySkill GitHub Repository](https://github.com/nyluke/subwayskill) <br>
- [MTA Data API](https://api.mta.info/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text transit summaries or structured JSON from the subwayskill CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include station names, routes, directions, departure times, source labels, and station suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
