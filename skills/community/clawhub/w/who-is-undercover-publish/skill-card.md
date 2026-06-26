## Description: <br>
Provides an OpenClaw skill for playing the social deduction game Who Is Undercover with configurable player counts, AI opponents, descriptions, voting, and game status commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq5776569](https://clawhub.ai/user/qq5776569) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to run a command-driven Who Is Undercover party game with human and AI players. It supports starting games, joining sessions, submitting descriptions, voting, checking status, and ending play. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package contains under-disclosed remote-service code and an embedded API key. <br>
Mitigation: Review the package before installation, remove or rotate the key, and run the InStreet controller only when contacting that external service is intended. <br>
Risk: Local scripts can change game state files while presenting status or automation behavior. <br>
Mitigation: Run the skill in an isolated workspace and separate read-only status inspection from state-changing automation before deployment. <br>
Risk: Network and data-handling behavior is not clearly documented for the extra remote-service path. <br>
Mitigation: Document any external service calls and data sent before enabling the remote-service integration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qq5776569/who-is-undercover-publish) <br>
- [Publisher profile](https://clawhub.ai/user/qq5776569) <br>
- [Project homepage from ClawHub metadata](https://github.com/long5/who-is-undercover) <br>
- [InStreet skills page](https://instreet.com/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Command responses and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Game output may include role, word, round, vote, player, and status information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, skill frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
