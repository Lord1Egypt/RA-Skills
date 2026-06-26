## Description: <br>
Query WhatPulse computer usage statistics using natural language, including keystrokes, mouse activity, application screen time, network bandwidth, website tracking, uptime, and profiles from a local read-only SQLite database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smitmartijn](https://clawhub.ai/user/smitmartijn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and WhatPulse users use this skill to ask natural language questions about local computer activity history and receive summarized statistics from the WhatPulse database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private WhatPulse activity history, including application usage, websites, input counts, and network patterns. <br>
Mitigation: Install only when that activity history is appropriate for the agent to read and summarize. <br>
Risk: Pointing WHATPULSE_DB at the wrong file or a shared location can expose unintended activity data. <br>
Mitigation: Keep WHATPULSE_DB set only to the intended database and avoid synced or shared storage unless it is private and access-controlled. <br>
Risk: Remote or scheduled snapshot workflows can persist sensitive usage data outside the original device. <br>
Mitigation: Do not use the cron or cloud snapshot workflow on sensitive or managed systems without confirming where the copied database will persist. <br>


## Reference(s): <br>
- [WhatPulse](https://whatpulse.org) <br>
- [ClawHub release page](https://clawhub.ai/smitmartijn/whatpulse-ai-agent-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with sqlite3 shell command examples and tabular summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only sqlite3 queries against a user-selected WhatPulse database.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
