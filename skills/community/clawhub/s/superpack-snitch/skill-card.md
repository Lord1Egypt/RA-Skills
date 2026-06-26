## Description: <br>
Soft blocklist guard for OpenClaw that injects a security directive at agent bootstrap and warns on incoming messages that reference blocked terms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rgr4y](https://clawhub.ai/user/rgr4y) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add a configurable soft blocklist policy to agent sessions, including bootstrap guidance and incoming-message warnings for blocked terms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The global soft blocklist may interfere with package-management or tool workflows that mention blocked terms. <br>
Mitigation: Review the default blocklist before installation and adjust SNITCH_BLOCKLIST or remove the skill when those workflows are required. <br>
Risk: Soft enforcement depends on agent adherence to injected guidance and warning messages. <br>
Mitigation: Use additional hard enforcement controls when actual tool-call blocking is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rgr4y/superpack-snitch) <br>
- [Publisher Profile](https://clawhub.ai/user/rgr4y) <br>
- [Plugin README Linked From Skill Documentation](https://github.com/rgr4y/superpack-snitch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown policy text and warning messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the SNITCH_BLOCKLIST environment variable when configured; defaults include clawhub and clawdhub.] <br>

## Skill Version(s): <br>
0.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
