## Description: <br>
Chat with Trump - respond in Trump's voice using his real quotes and speech patterns. Use when user wants to talk to Trump or asks Trump-like questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwwttlll](https://clawhub.ai/user/wwwttlll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill for Trump-style political roleplay that draws on a local quote database and persona prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to produce partisan, aggressive, and potentially false political persona responses. <br>
Mitigation: Use it only for intentional roleplay and verify factual political claims with independent sources. <br>
Risk: The skill uses Bash for local quote lookup. <br>
Mitigation: Review the bundled Python scripts before installation or execution. <br>
Risk: Support prompts can write generated persona content inside the skill directory. <br>
Mitigation: Run the skill in a workspace where skill-directory changes can be reviewed before reuse or release. <br>


## Reference(s): <br>
- [Trump Skill on ClawHub](https://clawhub.ai/wwwttlll/trump-skill) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Trump Persona Prompt](artifact/prompts/trump_persona.md) <br>
- [AgentSkills Standard](https://agentskills.io) <br>
- [Claude Code](https://claude.ai/code) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Plain text chat responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persona responses may include partisan, inflammatory, or false political claims and should be fact-checked outside the skill.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
