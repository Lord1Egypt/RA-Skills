## Description:

Access Wahoo Fitness Cloud API to fetch workouts, download FIT files, and analyze training data (power, HR, cadence, GPS).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tgmerritt](https://clawhub.ai/user/tgmerritt)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to connect to Wahoo Fitness Cloud, synchronize workout data, parse FIT files, and answer training questions from a local SQLite database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth tokens and detailed workout or GPS data may be exposed on shared machines, synced folders, or agent workspaces.

Mitigation: Use a private WAHOO_BASE_DIR with restrictive permissions and avoid placing the database, FIT files, or token files in shared locations.

Risk: OAuth setup output and logs can reveal sensitive authentication details.

Mitigation: Avoid logging OAuth setup sessions or sharing terminal output from authorization and token setup.

Risk: The default OAuth scopes may be broader than a user's immediate task requires.

Mitigation: Reduce WAHOO_SCOPES where possible before authorizing the skill.

Risk: Dependency installation may be fragile because the dependency name and version are not pinned in requirements.txt.

Mitigation: Fix and pin the FIT parsing dependency before running pip install in a production or shared environment.

## Reference(s):

- [Wahoo Fitness Cloud API](https://cloud-api.wahooligan.com/)
- [ClawHub Skill Page](https://clawhub.ai/tgmerritt/skills/wahoo-cloud)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, SQL examples, configuration guidance, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local OAuth token files, FIT downloads, and a SQLite workout database when the documented commands are run.]

## Skill Version(s):

0.2.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
