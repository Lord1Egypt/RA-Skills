## Description: <br>
Interact with teemtape stock watchlists and anonymous notes via the teemtape CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiwifellows](https://clawhub.ai/user/kiwifellows) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run the teemtape CLI for delayed quote lookup, ticker search, watchlist management, and reading or posting anonymous stock notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a networked CLI that requires a teemtape watchlist token and can reveal share URLs. <br>
Mitigation: Install only when agents should access teemtape, keep TEEMTAPE_TOKEN and share URLs out of chat logs, and avoid echoing secrets. <br>
Risk: CLI notes are anonymous comments that may be visible to other watchlist viewers. <br>
Mitigation: Read existing notes before posting, keep notes concise, and confirm before asking an agent to publish a note. <br>
Risk: Quote data is delayed and informational only. <br>
Mitigation: Do not use the skill as a trading tool or present quote output as real-time investment advice. <br>


## Reference(s): <br>
- [teemtape CLI command reference](references/commands.md) <br>
- [teemtape CLI JSON output shapes](references/json-output.md) <br>
- [teemtape skill page](https://clawhub.ai/kiwifellows/skills/teemtape-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs agents to prefer --json output and to treat TEEMTAPE_TOKEN and share URLs as sensitive.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
