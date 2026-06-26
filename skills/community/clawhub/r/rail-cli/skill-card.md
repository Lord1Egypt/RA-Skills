## Description: <br>
Rail CLI helps agents query UK National Rail departures, arrivals, station search, destination filtering, batch station lookup, and lightweight field selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shan8851](https://clawhub.ai/user/shan8851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and agents use this skill to install and operate the rail CLI for UK rail board checks, station resolution, destination filtering, and batch station search. <br>

### Deployment Geography for Use: <br>
Global; the rail data coverage described by the skill is National Rail stations in Great Britain. <br>

## Known Risks and Mitigations: <br>
Risk: Departures and arrivals require DARWIN_ACCESS_TOKEN, which is a sensitive credential. <br>
Mitigation: Store the token in environment configuration, avoid exposing it in prompts or logs, and only run the CLI in contexts where that credential access is intended. <br>
Risk: Live rail results depend on National Rail Darwin or the configured Huxley2 upstream and may return ambiguity or upstream errors. <br>
Mitigation: Use the CLI's structured error envelopes, retry only when appropriate, and prefer CRS codes when station names are ambiguous. <br>


## Reference(s): <br>
- [Rail CLI on ClawHub](https://clawhub.ai/shan8851/rail-cli) <br>
- [Rail CLI homepage](https://rail-cli.xyz) <br>
- [Install rail-cli (npm)](https://www.npmjs.com/package/@shan8851/rail-cli) <br>
- [National Rail Darwin OpenLDBWS registration](https://realtime.nationalrail.co.uk/OpenLDBWSRegistration/Registration) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI results are text or JSON envelopes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the rail binary; departures and arrivals require DARWIN_ACCESS_TOKEN; station search works without a token.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
