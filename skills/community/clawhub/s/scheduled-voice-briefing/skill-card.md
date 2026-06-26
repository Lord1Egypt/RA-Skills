## Description: <br>
Turns natural language requests into scheduled voice notification configurations and bounded structured briefing text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunxq1017-hash](https://clawhub.ai/user/sunxq1017-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create or update recurring or one-time spoken notification schedules, define modules such as environment or schedule summaries, and generate bounded briefing text for runtime voice delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted templates or object-rich contexts could expose sensitive data or produce unsafe briefing content. <br>
Mitigation: Use trusted template files, provide only the context data needed for the briefing, and review generated configuration changes before runtime use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunxq1017-hash/scheduled-voice-briefing) <br>
- [Config Schema](references/config-schema.md) <br>
- [Briefing Templates](references/briefing-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON configuration examples, Python helper scripts, and generated briefing text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are bounded by configured modules; voice playback and external data are supplied by the runtime environment.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
