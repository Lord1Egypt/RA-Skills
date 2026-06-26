## Description: <br>
Retrieves sports events, fixtures, results, team information, and league details across multiple sports using TheSportsDB free API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mingo-318](https://clawhub.ai/user/Mingo-318) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to answer sports schedule, result, league, and team-information requests by querying TheSportsDB from a local Python command-line helper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sports query terms are sent to TheSportsDB. <br>
Mitigation: Avoid entering private or sensitive search terms and review TheSportsDB usage expectations before use. <br>
Risk: The helper depends on the Python requests package. <br>
Mitigation: Install dependencies in a virtual environment and review dependency sources before running the script. <br>
Risk: Some command output labels are in Chinese. <br>
Mitigation: Confirm output meaning before relying on results in user-facing or operational workflows. <br>


## Reference(s): <br>
- [TheSportsDB API](https://www.thesportsdb.com/) <br>
- [ClawHub skill page](https://clawhub.ai/Mingo-318/sports-events-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sports event lists, scores, team details, league names, and brief status or error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
