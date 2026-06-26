## Description: <br>
Run the installed red-crawler CLI for Xiaohongshu contact discovery. Requires the red-crawler command and Playwright browser runtime; not instruction-only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[batxent](https://clawhub.ai/user/batxent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run red-crawler workflows for Xiaohongshu creator discovery, login session handling, scheduled collection, reporting, and contactable creator exports from a local workspace database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser authentication, proxy credentials, and session-related details may appear in command output, job JSON, logs, or status results. <br>
Mitigation: Use a private workspace, avoid real credentials unless the exposure is acceptable, and keep storage-state files, job directories, logs, and databases out of shared folders and version control. <br>
Risk: The skill depends on the installed red-crawler binary and Playwright browser runtime. <br>
Mitigation: Install only a trusted red-crawler binary and review bootstrap flags before allowing dependency or browser installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/batxent/rednote-contacts) <br>
- [red-crawler project homepage](https://github.com/Batxent/red-crawler) <br>
- [Publisher profile](https://clawhub.ai/user/batxent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files] <br>
**Output Format:** [Structured status objects, command summaries, logs, and generated CSV or JSON artifact paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return background job identifiers, heartbeat state, stdout, stderr, metrics, reports, and contact export artifacts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
