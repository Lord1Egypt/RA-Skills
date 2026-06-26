## Description: <br>
Captures learnings, errors, corrections, feature requests, and recurring patterns so coding agents can review and promote durable guidance across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asterisk622](https://clawhub.ai/user/asterisk622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to capture corrections, command failures, feature requests, and non-obvious solutions as reusable learning records. It supports later review and promotion of verified learnings into project or workspace agent guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Learning logs and promoted memory may persist sensitive session details into future agent context. <br>
Mitigation: Keep logs local by default and redact tokens, credentials, personal data, customer data, and raw command payloads before logging or promotion. <br>
Risk: Broad or empty-matcher hooks can inject reminders on every prompt and expand the skill's influence beyond intended workflows. <br>
Mitigation: Enable hooks only in trusted workspaces and scope matchers to the events or commands that need learning capture. <br>
Risk: Unreviewed learning entries can promote incorrect or misleading guidance into agent instruction files. <br>
Mitigation: Review and scan entries before promotion; keep low-confidence entries pending until verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asterisk622/xiaoding-self-improving-agent) <br>
- [OpenClaw integration guide](references/openclaw-integration.md) <br>
- [Hook setup guide](references/hooks-setup.md) <br>
- [Self-improvement examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or updates of .learnings markdown files and reviewed agent instruction files.] <br>

## Skill Version(s): <br>
3.0.15 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
