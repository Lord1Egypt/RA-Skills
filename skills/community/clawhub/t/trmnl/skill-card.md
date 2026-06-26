## Description: <br>
Generate content for TRMNL e-ink display devices using the TRMNL CSS framework and send it via the trmnl CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peetzweg](https://clawhub.ai/user/peetzweg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and TRMNL users use this skill to create HTML display content, dashboard views, notifications, and messages for TRMNL e-ink devices and send them through configured custom plugin webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Custom plugin webhook URLs can expose access to a TRMNL display workflow if shared. <br>
Mitigation: Treat webhook URLs as sensitive and avoid including them in public prompts, logs, or generated display content. <br>
Risk: Installing trmnl-cli with @latest can change behavior between releases. <br>
Mitigation: Pin the npm CLI version when reproducible behavior is required. <br>
Risk: Generated content may include private or important information before it is sent to a display. <br>
Mitigation: Preview or validate content with trmnl validate before sending sensitive or important updates. <br>


## Reference(s): <br>
- [TRMNL Display release page](https://clawhub.ai/peetzweg/trmnl) <br>
- [TRMNL framework overview](references/framework-overview.md) <br>
- [TRMNL CSS utilities](references/css-utilities.md) <br>
- [TRMNL layout systems](references/layout-systems.md) <br>
- [TRMNL components](references/components.md) <br>
- [TRMNL display patterns](references/patterns.md) <br>
- [TRMNL webhook API](references/webhook-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces TRMNL framework HTML intended for validation and delivery through the trmnl CLI.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
