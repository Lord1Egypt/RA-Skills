## Description: <br>
Sync WaniKani Japanese learning progress data from the API to local SQLite storage for backup, offline analysis, statistics, review-pattern analysis, and level tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mart1n-xyz](https://clawhub.ai/user/mart1n-xyz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External WaniKani users and developers use this skill to sync their own WaniKani API data into a local SQLite database, then query progress, review statistics, level history, and problem items offline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync script needs a WaniKani API token. <br>
Mitigation: Provide the token through WANIKANI_API_TOKEN rather than a command-line argument, and do not commit or share the token. <br>
Risk: The local SQLite database contains a copy of the user's WaniKani learning progress data. <br>
Mitigation: Store wanikani.db in a private directory and keep it out of source control or shared folders. <br>
Risk: The skill runs local Python scripts and depends on the local Python environment. <br>
Mitigation: Install and run dependencies from a trusted environment before syncing data. <br>


## Reference(s): <br>
- [WaniKani API Structure Reference](references/api-structure.md) <br>
- [WaniKani Example Queries](references/example-queries.sql) <br>
- [WaniKani](https://www.wanikani.com) <br>
- [WaniKani API](https://api.wanikani.com/v2) <br>
- [WaniKani API Tokens](https://www.wanikani.com/settings/personal_access_tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Files, Guidance] <br>
**Output Format:** [Markdown with bash and SQL examples; Python scripts create and query a local SQLite database.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a WANIKANI_API_TOKEN; writes wanikani.db in the selected data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
