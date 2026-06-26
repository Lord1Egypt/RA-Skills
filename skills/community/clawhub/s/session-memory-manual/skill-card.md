## Description: <br>
Provides manually triggered cross-session memory search and synchronization for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoquan](https://clawhub.ai/user/guoquan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they explicitly ask an agent to search prior OpenClaw sessions or shared memory files, summarize relevant decisions or reminders, and synchronize selected notes into shared memory after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read prior OpenClaw sessions and expose information from earlier conversations. <br>
Mitigation: Use it only for explicit cross-session lookup requests, specify exact keywords, sessions, or time ranges, and review retrieved results before using them. <br>
Risk: User-approved memory writes could persist sensitive or overly broad information in shared memory. <br>
Mitigation: Approve only necessary notes, redact secrets and private details, and avoid storing passwords, API keys, private chats, or sensitive business information. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guoquan/session-memory-manual) <br>
- [Publisher Profile](https://clawhub.ai/user/guoquan) <br>
- [Homepage](https://github.com/openclaw/skills/session-memory-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with inline commands and file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose session-history lookup, memory-file search, and user-approved memory writes.] <br>

## Skill Version(s): <br>
0.5.6 (source: server release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
