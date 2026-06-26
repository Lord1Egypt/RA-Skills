## Description: <br>
Access sports data via TheSportsDB, including teams, events, and scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumadeiras](https://clawhub.ai/user/gumadeiras) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to look up sports teams, recent scores, and upcoming fixtures through TheSportsDB API examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The TheSportsDB API key could be exposed through shell history, logs, or shared command output. <br>
Mitigation: Store THE_SPORTS_DB_KEY in the local environment file, restrict access to that file, and avoid sharing logs or command output that include expanded API URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gumadeiras/the-sports-db) <br>
- [TheSportsDB search team API example](https://www.thesportsdb.com/api/v1/json/$THE_SPORTS_DB_KEY/searchteams.php?t=Palmeiras) <br>
- [TheSportsDB last events API example](https://www.thesportsdb.com/api/v1/json/$THE_SPORTS_DB_KEY/eventslast.php?id=134465) <br>
- [TheSportsDB next events API example](https://www.thesportsdb.com/api/v1/json/$THE_SPORTS_DB_KEY/eventsnext.php?id=134465) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires THE_SPORTS_DB_KEY and is subject to a documented 30 requests per minute rate limit.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
