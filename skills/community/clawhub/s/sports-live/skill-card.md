## Description: <br>
Aggiornamenti sportivi in tempo reale tramite TheSportsDB e API-Football. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jakah2551](https://clawhub.ai/user/jakah2551) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up live scores, today's matches, recent results, upcoming team fixtures, and team or player search results across supported sports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an included Python script and makes network requests to external sports APIs. <br>
Mitigation: Install only in environments where Python execution and outbound requests to TheSportsDB and API-Football are acceptable. <br>
Risk: Football-specific commands require a private API-Football key. <br>
Mitigation: Treat the key as sensitive, do not ask the agent to print it, and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jakah2551/sports-live) <br>
- [TheSportsDB API endpoint](https://www.thesportsdb.com/api/v1/json/1/) <br>
- [API-Football registration](https://dashboard.api-football.com/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style text with command-backed sports results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on live responses from TheSportsDB and API-Football; football-specific commands require a private API-Football key.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
