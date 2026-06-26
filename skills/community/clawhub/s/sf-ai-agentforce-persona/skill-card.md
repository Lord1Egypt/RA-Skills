## Description: <br>
Designs Salesforce Agentforce agent personas, sample dialogs, scoring artifacts, and Agentforce encoding guidance from brand inputs, persona documents, URLs, or text descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dsouza-anush](https://clawhub.ai/user/dsouza-anush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, admins, and developers use this skill to create consistent Agentforce personas, validate the voice through sample dialog, score persona quality, and produce Agentforce Builder or Agent Script encoding guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated persona, sample dialog, scorecard, and encoding files may persist locally under _local/generated. <br>
Mitigation: Avoid confidential brand guides or internal prompts unless local persistence is acceptable, and review generated files before sharing or deploying them. <br>
Risk: Voice or telephony work may rely on inferred voice attributes when the user does not specify them. <br>
Mitigation: Explicitly choose or confirm voice attributes, including gender-related choices, during voice persona design. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dsouza-anush/sf-ai-agentforce-persona) <br>
- [Publisher profile](https://clawhub.ai/user/dsouza-anush) <br>
- [Agent Persona Framework](artifact/references/persona-framework.md) <br>
- [Persona Encoding Guide](artifact/references/persona-encoding-guide.md) <br>
- [Voice Encoding Guide](artifact/references/persona-encoding-guide-voice.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown files and inline Agentforce configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write persona documents, sample dialogs, scorecards, and Agentforce encoding outputs under _local/generated when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata); source workflow 2.4.0 (source: SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
