## Description: <br>
Helps create and manage OpenClaw subagents with independent workspaces, dedicated skill directories, configuration files, and Feishu channel integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[google-q-dot](https://clawhub.ai/user/google-q-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to scaffold subagent workspaces, copy required skills, configure OpenClaw agent settings, and connect each subagent to a Feishu bot/channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Created agents may forward all messages to Feishu without filtering, which can expose sensitive task content or status updates. <br>
Mitigation: Modify the generated messaging rules before use so only approved, non-sensitive updates are sent to Feishu. <br>
Risk: Feishu app credentials and bot bindings may be copied into shared configuration without clear access or rotation controls. <br>
Mitigation: Use least-privilege Feishu credentials, avoid shared plaintext secrets where possible, and document credential rotation and per-agent controls. <br>
Risk: Users may not expect all subagent communications to be relayed to an external chat channel. <br>
Mitigation: Document consent, redaction, and channel-scoping requirements before enabling Feishu bindings for created agents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/google-q-dot/subagent-creator) <br>
- [Publisher profile](https://clawhub.ai/user/google-q-dot) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON, bash, Python, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-readable setup guidance for creating subagent directories, OpenClaw configuration entries, Feishu bot bindings, and invocation examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, artifact/_meta.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
