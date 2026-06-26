## Description: <br>
Structures technical-topic debates across pro, con, and judge roles, with multi-phase argument rounds, user intervention between phases, and a final consensus, disagreement, and practical recommendation summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suran7810](https://clawhub.ai/user/suran7810) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical decision makers use this skill to run structured debates about technical choices, surface opposing arguments, incorporate user-supplied perspectives, and produce decision-oriented consensus and recommendation summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad debate phrasing and generate persuasive or misleading technical guidance if the topic is underspecified. <br>
Mitigation: Provide a concrete technical topic, review the pro and con claims, and validate final recommendations before using them for decisions. <br>
Risk: Sensitive proprietary topics discussed in the debate remain part of the current agent session. <br>
Mitigation: Avoid entering confidential or proprietary details unless they are appropriate for the active agent session. <br>


## Reference(s): <br>
- [Output Format](references/output-format.md) <br>
- [Prompt Templates](references/prompts.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/suran7810/tech-debate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown debate transcript with phase summaries, intervention prompts, and a final consensus report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primarily Chinese-language output; topic is required and max rounds per phase defaults to 5 when not specified.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
