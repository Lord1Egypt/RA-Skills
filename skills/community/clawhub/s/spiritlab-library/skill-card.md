## Description: <br>
Agent enhancer with 160K+ battle-tested engineering patterns, library-first search, knowledge base access, project memory, AI search routing, and security-aware developer tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyigang1969](https://clawhub.ai/user/liyigang1969) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route technical questions through the SpiritLab library before falling back to broader search, preserving project context and recording unresolved search gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plain-HTTP remote service use can expose registration, search, heartbeat, or bootstrap traffic to interception or modification. <br>
Mitigation: Use only in workspaces where plain-HTTP traffic is acceptable, and prefer a release that uses HTTPS with integrity checks for downloaded content. <br>
Risk: Bootstrap can download remote content and write it into local agent control files, changing future agent behavior. <br>
Mitigation: Do not run --bootstrap in sensitive workspaces unless downloaded changes can be reviewed first; keep backups and inspect diffs before reuse. <br>
Risk: Heartbeat can upload saved search gaps and registration data to the remote service. <br>
Mitigation: Avoid --heartbeat when query text or workspace identifiers may be sensitive, and provide controls to inspect and delete stored gap data before upload. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liyigang1969/spiritlab-library) <br>
- [Publisher Profile](https://clawhub.ai/user/liyigang1969) <br>
- [SpiritLab Homepage](https://spiritlab.top) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a remote plain-HTTP service for registration, search, heartbeat, bootstrap, and upgrade operations.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
