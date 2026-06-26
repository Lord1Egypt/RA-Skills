## Description: <br>
Hotel search and pricing via the RollingGo CLI for searching hotels by destination, filtering by date, star rating, budget, tags, or distance, inspecting hotel details and room pricing, and looking up hotel tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rollinggo-ai](https://clawhub.ai/user/rollinggo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, travel agents, and developers use this skill to search hotel candidates, compare current pricing and room details, retrieve hotel tags, and produce commands that query the RollingGo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RollingGo API key, and exposing credentials in commands or host-wide configuration can leak sensitive access. <br>
Mitigation: Use per-skill secret injection where possible, avoid pasting real API keys directly into commands, and keep host-wide environment configuration limited to trusted contexts. <br>
Risk: The default runtime uses the latest rollinggo package on each run, which can change behavior without review. <br>
Mitigation: For sensitive workflows, review or pin a specific rollinggo package version before execution. <br>


## Reference(s): <br>
- [RollingGo Homepage](https://rollinggo.store) <br>
- [ClawHub Skill Page](https://clawhub.ai/rollinggo-ai/rollinggo-hotel-booking-skill) <br>
- [RollingGo NPX Reference](references/rollinggo-npx.md) <br>
- [RollingGo UV Reference](references/rollinggo-uv.md) <br>
- [Claw Host Environment Reference](references/claw-host-env.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide CLI execution that returns JSON result payloads, booking URLs, hotel detail links, and stderr errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
