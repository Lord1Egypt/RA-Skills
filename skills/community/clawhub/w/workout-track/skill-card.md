## Description: <br>
Log a strength training session and insert it into the life_db database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spideystreet](https://clawhub.ai/user/spideystreet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to record strength training sessions from natural language. The agent parses workout details, asks for confirmation, and stores confirmed sessions in a PostgreSQL sport schema. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes workout records to a user-configured PostgreSQL life_db using local database credentials. <br>
Mitigation: Verify the .env file points to the intended database and use a database user limited to the sport schema. <br>
Risk: The skill runs a shell command to execute the insert script. <br>
Mitigation: Approve saves only after checking the agent's recap of the parsed workout fields. <br>


## Reference(s): <br>
- [Workout Track ClawHub page](https://clawhub.ai/spideystreet/workout-track) <br>
- [README](artifact/README.md) <br>
- [Database schema](artifact/schema.sql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Plain text or Markdown recap, followed by a shell command that runs the insert script with a minified JSON payload after user confirmation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, PostgreSQL credentials in the configured environment file, and user confirmation before saving.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
