## Description: <br>
Twinify creates consent-based AI digital twin agents from WhatsApp chat exports by parsing messages and guiding profile-file generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neobotjan2026](https://clawhub.ai/user/neobotjan2026) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use Twinify to create AI simulations of people who have explicitly consented to being modeled from WhatsApp chat history. The skill supports local chat parsing, personality analysis, and generation of SOUL, EXAMPLES, ANTI-EXAMPLES, MEMORY, and AGENTS guidance files for an OpenClaw agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes private WhatsApp chat exports and generated profile files may expose personal data. <br>
Mitigation: Use only when the modeled person and affected chat participants understand and consent; redact private details, process locally, keep files private, and delete parsed/profile data when consent is withdrawn. <br>
Risk: The generated agent can deceptively present as a real person. <br>
Mitigation: Change the generated instructions so the agent clearly identifies as an AI simulation, and do not use it for impersonation, harassment, deception, or other harmful uses. <br>


## Reference(s): <br>
- [AGENTS.md Template](references/agents-guide.md) <br>
- [ANTI-EXAMPLES.md Generation Guide](references/anti-examples-guide.md) <br>
- [EXAMPLES.md Generation Guide](references/examples-guide.md) <br>
- [MEMORY.md Generation Guide](references/memory-guide.md) <br>
- [SOUL.md Generation Guide](references/soul-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python parser output, JSON parsed-message files, and profile documents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can contain sensitive personal data from chat exports and generated persona profiles.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
