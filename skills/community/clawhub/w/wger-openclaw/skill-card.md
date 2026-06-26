## Description: <br>
Manage gym routines, log workouts, track nutrition, update goals, and generate fitness reports via the wger API integrated with OpenClaw automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xjaspreet](https://clawhub.ai/user/0xjaspreet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to wger for routine lookup, workout and nutrition logging, goal updates, and progress reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a wger API token for account access. <br>
Mitigation: Keep WGER_TOKEN private and provide it through the environment rather than embedding it in prompts, files, or shared command history. <br>
Risk: Workout, nutrition, or routine updates can write data to a user's wger account. <br>
Mitigation: Review the exact API payload before logging workouts or nutrition entries or updating routines. <br>
Risk: The self-hosting example includes a sample Docker database password. <br>
Mitigation: Replace the sample password with a strong secret before running a self-hosted deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/0xjaspreet/wger-openclaw) <br>
- [wger API Endpoints Reference](references/api_endpoints.md) <br>
- [Self-Host wger](references/selfhost.md) <br>
- [wger API documentation](https://wger.readthedocs.io/en/latest/api.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the wger API and return JSON responses or human-readable workout, nutrition, and progress summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
