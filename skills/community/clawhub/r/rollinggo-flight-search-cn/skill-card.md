## Description: <br>
Uses the RollingGo Flight CLI to look up airport codes and search flight results by route, date, cabin class, trip type, and passenger counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rollinggo-ai](https://clawhub.ai/user/rollinggo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, travel planners, and developers use this skill to convert flight-search requests into RollingGo CLI airport-code lookups and structured flight searches. It helps compare available flights for one-way or round-trip travel, while leaving booking, payment, check-in, and seat selection outside scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes standalone installer examples that pipe remote scripts into a shell. <br>
Mitigation: Prefer the npm or uv package-manager paths, or inspect and pin any installer script before running it. <br>
Risk: The skill requires ROLLINGGO_API_KEY and may expose it through command-line arguments or shared logs if handled loosely. <br>
Mitigation: Provide the API key through secret or environment configuration, avoid passing it on the command line, and redact it from logs and transcripts. <br>
Risk: Flight origins, destinations, dates, passenger counts, and cabin choices are sent to RollingGo for processing. <br>
Mitigation: Share only travel details intended for RollingGo and avoid entering sensitive personal information that is not required for search. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rollinggo-ai/rollinggo-flight-search-cn) <br>
- [RollingGo homepage](https://rollinggo.store) <br>
- [RollingGo API key application](https://rollinggo.store/apply) <br>
- [RollingGo Flight NPX Reference](references/rollinggo-flight-npx.md) <br>
- [RollingGo Flight UVX Reference](references/rollinggo-flight-uvx.md) <br>
- [RollingGo Flight Workflows](references/flight-workflows.md) <br>
- [Claw Host Environment Reference](references/claw-host-env.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The RollingGo CLI returns flight and airport results on stdout, usually as JSON, with errors on stderr.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
