## Description: <br>
Access Wahoo Fitness Cloud API to fetch workouts, download FIT files, and analyze training data (power, HR, cadence, GPS). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tgmerritt](https://clawhub.ai/user/tgmerritt) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to connect to a user's Wahoo Fitness Cloud account, synchronize workout metadata, download FIT files, and analyze training data in a local SQLite database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wahoo OAuth tokens, FIT files, workout history, heart-rate and power data, and GPS traces are stored locally. <br>
Mitigation: Set WAHOO_BASE_DIR to a private, non-synced location, keep it out of source control, and avoid untrusted backups. <br>
Risk: Interactive OAuth setup can expose redirect URLs or authorization codes in shared terminal output. <br>
Mitigation: Run OAuth setup in a private terminal and avoid sessions whose output is logged or shared. <br>
Risk: Installing the Python dependency changes the local environment. <br>
Mitigation: Review requirements.txt before installing and use an isolated Python environment when practical. <br>


## Reference(s): <br>
- [Wahoo Fitness Cloud API](https://cloud-api.wahooligan.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/tgmerritt/wahoo-cloud) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, SQL snippets, and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Wahoo OAuth credentials and writes tokens, FIT files, and a SQLite workout database under WAHOO_BASE_DIR.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
