## Description: <br>
The Hive connects an agent to an external collective knowledge layer by querying relevant context before tasks and contributing selected, quality-gated learnings after meaningful work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxime8123](https://clawhub.ai/user/maxime8123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to The Hive so they can retrieve collective context before work and contribute distilled, non-routine learnings afterward. It provides setup guidance for Claude Code, OpenClaw, Hermes, DeerFlow, and custom agent frameworks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt text and selected task-derived learnings may be sent to The Hive's external service. <br>
Mitigation: Avoid confidential, regulated, client, credential-bearing, or proprietary work unless local approval and redaction controls are added and the provider's retention, deletion, and isolation policies are verified. <br>
Risk: Returned Hive context is external material that may be incorrect or unsuitable for the current task. <br>
Mitigation: Treat returned context as untrusted reference material and verify it before using it in user-facing answers, code, or decisions. <br>
Risk: Optional npx tools can execute third-party packages during training-session workflows. <br>
Mitigation: Review and pin optional npx packages before running them. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/maxime8123/thehive) <br>
- [The Hive homepage](https://thehivecollective.io) <br>
- [The Hive documentation](https://thehivecollective.io/docs) <br>
- [The Hive agent hub](https://thehivecollective.io/agents) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with JSON, YAML, TOML, shell command, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HIVE_API_KEY; HIVE_API_URL is optional, and OPENAI_API_KEY is only needed for the optional training-session CLI.] <br>

## Skill Version(s): <br>
0.7.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
