## Description: <br>
RSS摘要工具免费版 helps personal users scan RSS feeds, filter high-signal unread entries, and synthesize grouped summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External individual users use this skill to review RSS subscriptions, identify relevant unread articles, and produce concise daily or topic-focused digests. It also helps inspect feed health, search stored feed content, and keep unread queues manageable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external feed CLI and may require source-based installation. <br>
Mitigation: Verify the feed CLI source before installing and confirm that the local runtime meets the documented dependency requirements. <br>
Risk: Fetching RSS entries and article pages contacts external feed and website hosts. <br>
Mitigation: Use trusted feeds, review network access expectations before running fetch commands, and avoid sending sensitive URLs or private feed content to untrusted services. <br>
Risk: Commands can mark entries as read, changing the user's local RSS state. <br>
Mitigation: Only mark entries as read after explicit user confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/rss-digest-tool-free) <br>
- [Rust toolchain](https://rustup.rs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries are limited by the free edition guidance to 5-10 selected entries per digest.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
