## Description: <br>
SBTI 人格测评 guides users through a Chinese entertainment personality quiz, calculates 15-dimension scores, and returns one of 27 personality types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mydearzsy](https://clawhub.ai/user/mydearzsy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run a casual SBTI personality quiz, collect answer choices, calculate scores with the bundled local script, and present an entertainment-only result. It can also provide answer guidance for a requested type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The quiz includes crude humor and personal-style questions about feelings, relationships, and self-image. <br>
Mitigation: Present results as entertainment only, let users skip uncomfortable questions, and avoid treating outputs as psychological, medical, or hiring guidance. <br>
Risk: The skill may run a bundled local Python calculator. <br>
Mitigation: Review scripts/calculate.py before execution and run it only in a trusted local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mydearzsy/silly-big-type) <br>
- [SBTI complete question bank](references/questions.md) <br>
- [SBTI personality type definitions](references/types.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with quiz prompts, scored dimensions, personality code/name, similarity, and short result description.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The calculator expects 30 comma-separated numeric answers in Q1-Q30 order and prints a formatted result.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
