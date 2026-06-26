## Description: <br>
A self-learning and error-prevention skill that guides an agent to record mistakes, analyze root causes, maintain checklists, and review progress to reduce repeated errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add structured self-review, error logging, root-cause analysis, prevention checklists, and periodic retrospectives to an AI assistant workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning and error records may capture secrets, private prompts, credentials, or sensitive project details. <br>
Mitigation: Require explicit user consent for persistent records, redact sensitive content, and prohibit storing secrets or credentials in logs. <br>
Risk: The skill encourages credential-related handling, repository operations, external research, browser automation, and login/session use. <br>
Mitigation: Require explicit confirmation before external research, repository clone, login/session use, token lookup, browser automation, or scheduled review actions. <br>
Risk: Automatic note updates and scheduled retrospectives can change ongoing agent behavior without clear user awareness. <br>
Mitigation: Keep review storage scoped and visible, allow the user to pause or delete learning records, and avoid background updates without confirmation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/davidme6/self-learning-skill-v2) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Artifact error log](artifact/ERROR_LOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with checklists, templates, and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ongoing review notes, error records, learning summaries, and prevention checklists when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
