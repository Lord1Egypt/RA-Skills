## Description: <br>
Cross-session memory sync protocol. Ensures memory consistency across Feishu, webchat, and any other channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdt328606](https://clawhub.ai/user/sdt328606) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to keep shared memory, daily logs, current task state, and recent decisions synchronized across Feishu, webchat, and other sessions. It is intended for users who want continuity when work moves between communication channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes conversation details, task state, decisions, channel names, and session identifiers to shared persistent memory files that can be reused by later sessions. <br>
Mitigation: Install it only when cross-session memory sharing is intentional, avoid using it for sensitive work, and review or restrict access to the memory directory. <br>
Risk: Cross-channel synchronization can expose prior session context without clear per-session consent or containment. <br>
Mitigation: Prefer explicit user confirmation before syncing, consolidating, or archiving logs, and redact sensitive details before writing shared memory. <br>
Risk: The cleanup script archives dated memory logs rather than deleting their contents. <br>
Mitigation: Review logs before archiving and ensure archive retention and access controls match the workspace's privacy expectations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sdt328606/session-memory-sync) <br>
- [Publisher profile](https://clawhub.ai/user/sdt328606) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operating guidance for shared memory files and an optional cleanup script for archiving dated logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
