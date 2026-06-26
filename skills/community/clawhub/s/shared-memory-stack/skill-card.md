## Description: <br>
Complete reference for a shared memory architecture connecting Claude Code, OpenClaw/Kimi, and LM Studio subagents through an Obsidian vault and MemPalace index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerua1](https://clawhub.ai/user/nerua1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to understand and operate a local shared memory stack for multi-agent collaboration, including memory search, idea capture, vault indexing, and inter-agent communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent shared memory can expose secrets, client data, or private notes if sensitive content is stored in indexed folders. <br>
Mitigation: Keep sensitive information out of indexed vault paths, review vault contents before indexing, and restrict who can write to the shared memory folders. <br>
Risk: Shared vault and local gateway workflows can allow unintended cross-agent data sharing. <br>
Mitigation: Limit access to trusted local agents and users, keep the gateway local, and review shared files before agents rely on them. <br>
Risk: Publishing commands may make skill contents public using configured GitHub credentials. <br>
Mitigation: Do not run publishing commands unless public release is intended, and manually review files and credential configuration before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nerua1/shared-memory-stack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents local file paths, memory indexing, idea capture, inter-agent messaging, and publishing workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
