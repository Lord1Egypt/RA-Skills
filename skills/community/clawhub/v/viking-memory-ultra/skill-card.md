## Description: <br>
Viking Memory System Ultra is a layered memory system for agents, with semantic promotion, weighted retrieval, reversible archiving, review tracking, and command guidance for writing, reading, finding, loading, promoting, weighting, and compressing memories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsangho](https://clawhub.ai/user/tsangho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide agents in maintaining long-lived layered work memories, including daily notes, hot/warm/cold/archive retention, review status, shared important memories, and retrieval or compression workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived and shared memories can expose credentials, personal data, private notes, or confidential business context if agents save too much by default. <br>
Mitigation: Set clear rules for what may be saved or shared, avoid sensitive material, and require confirmation before syncing important content to shared memory. <br>
Risk: External sv_* scripts and API-assisted scanning or promotion may read, move, compress, or share memory content in ways users do not expect. <br>
Mitigation: Review the external scripts and configuration before use, run dry-run modes where available, and require confirmation before global sync or API-based scanning. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tsangho/viking-memory-ultra) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and frontmatter conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to create and maintain memory files across hot, warm, cold, archive, daily, long-term, meetings, and shared memory locations.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
