## Description: <br>
Wahoo Fitness Cloud API - fetch workouts, download FIT files, parse power/HR/cadence/GPS into local SQLite for analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tgmerritt](https://clawhub.ai/user/tgmerritt) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, agents, and fitness-data analysts use this skill to connect to a user's Wahoo account, sync workout metadata and FIT files, and query locally stored cycling telemetry for training analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wahoo OAuth tokens, client secrets, and refresh tokens are sensitive credentials that can grant access to a user's Wahoo data. <br>
Mitigation: Store credentials only in local environment or secret files, keep token files private, avoid pasting secrets into chats or logs, and revoke the Wahoo app or delete the token file when access is no longer needed. <br>
Risk: Synced workout databases and FIT files can include GPS tracks, heart-rate history, power data, device details, and other personal fitness information. <br>
Mitigation: Keep the training directory private, avoid sharing generated databases or logs, and tighten local directory permissions on shared machines. <br>
Risk: Wahoo API access may be limited by sandbox or production rate limits, especially during a first sync of long workout history. <br>
Mitigation: Use the built-in backoff behavior, expect long first-sync runs, and avoid increasing request frequency beyond documented Wahoo limits. <br>


## Reference(s): <br>
- [ClawHub Wahoo Skill release](https://clawhub.ai/tgmerritt/wahoo-skill) <br>
- [Wahoo Fitness Cloud API](https://cloud-api.wahooligan.com/) <br>
- [Wahoo Developer Portal](https://developers.wahooligan.com) <br>
- [fitparse FIT decoder](https://github.com/dtcooper/python-fitparse) <br>
- [Database schema](schema/wahoo_db_schema.sql) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands, SQL queries, JSON examples, and local SQLite/FIT file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Wahoo developer app, OAuth credentials, and local storage for tokens, FIT files, and SQLite workout data.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
