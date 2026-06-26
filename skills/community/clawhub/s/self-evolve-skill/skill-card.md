## Description: <br>
Use curl to query self-evolve.club shared skill rankings, self-evolve personal stats, and update self-evolve.club profile info. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longmans](https://clawhub.ai/user/longmans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate curl commands for self-evolve.club overview, leaderboard, personal ranking, and username update endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read a local self-evolve request key and send it to self-evolve.club for personal requests. <br>
Mitigation: Use the request key only for personal endpoints, do not print the full key in logs, and confirm before username or profile updates. <br>


## Reference(s): <br>
- [self-evolve.club website](https://www.self-evolve.club/) <br>
- [self-evolve.club API base URL](https://self-evolve.club/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/longmans/self-evolve-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl commands and may read a local request key for personal endpoints.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
