## Description: <br>
SRS evaluates security research tasks, matches them to operational roles, and supports knowledge-base review, task handoff, and parallel task execution workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caidongyun](https://clawhub.ai/user/caidongyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security researchers, SecOps teams, and knowledge managers use SRS to score incoming security research tasks, assign them to roles, review local research notes, and record follow-up work. It is most relevant for teams organizing OpenClaw or AI-security research workflows that involve local workspace scans and generated task files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans broad local research and OpenClaw workspace directories, which may expose sensitive local files to task review logic. <br>
Mitigation: Run it in a sandbox or dedicated non-sensitive workspace and review the default paths before using scan, review, daily, evaluate, improve, or parallel execution commands. <br>
Risk: The skill creates persistent role, review, handoff, feedback, result, and TODO files that may retain details from local research workflows. <br>
Mitigation: Inspect generated state files regularly, avoid using sensitive source directories, and remove generated files that should not persist. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/caidongyun/srs) <br>
- [Publisher profile](https://clawhub.ai/user/caidongyun) <br>
- [OpenClaw Security Guide: Data Governance and Incident Response](artifact/reports/OpenClaw-Security-Guide-Data-Incident.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, JSON status and evaluation objects, and CLI-oriented shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may write persistent local files for roles, reviews, handoffs, feedback, execution results, and TODO entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
