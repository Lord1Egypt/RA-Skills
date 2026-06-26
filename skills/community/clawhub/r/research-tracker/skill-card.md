## Description: <br>
Manage and track autonomous AI research projects with state logging, instruction queues, agent coordination, and progress monitoring via SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[julian1645](https://clawhub.ai/user/julian1645) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to coordinate long-running autonomous research agents, track project state and progress, exchange instructions, and monitor attention signals through a local research-tracker CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on installing an external CLI from the 1645labs Homebrew tap or Go repository. <br>
Mitigation: Install only from trusted sources, and review or pin a release before important use. <br>
Risk: Research content is retained in a local SQLite database. <br>
Mitigation: Keep tasks narrowly scoped and avoid logging secrets or highly sensitive material. <br>


## Reference(s): <br>
- [Research Tracker ClawHub page](https://clawhub.ai/julian1645/research-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CLI usage guidance for local SQLite-backed project tracking; users should avoid logging secrets or highly sensitive material.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
