## Description: <br>
Fully automatic cross-session short-term memory system for OpenClaw that stores conversation summaries in Redis with semantic tag indexing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hualang-c](https://clawhub.ai/user/hualang-c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and operate a local Redis-backed memory layer that synchronizes transcript-derived summaries, retrieves recent memory, and searches semantic tags across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads raw OpenClaw transcript files and stores conversation-derived memory in Redis. <br>
Mitigation: Install only where users expect persistent local memory, narrow SESSIONS_DIR and MEMORY_USERS, and avoid confidential or multi-user sessions without consent, deletion, and access controls. <br>
Risk: The setup workflow installs persistent background jobs for memory synchronization and monitoring. <br>
Mitigation: Review the installed crontab after setup, keep Redis protected, and disable or scope scheduled jobs that are not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hualang-c/redis-memory-system) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/hualang-c) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Redis and configured OpenClaw transcript access; sync and retrieval commands operate on local files and Redis keys.] <br>

## Skill Version(s): <br>
3.3.0 (source: ClawHub release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
