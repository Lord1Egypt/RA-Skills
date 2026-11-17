## Description:

Tech Debate guides an agent to run a Chinese-language, multi-phase structured debate on a technical topic, with pro and con roles, neutral judge summaries, user interventions between phases, and a final consensus report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suran7810](https://clawhub.ai/user/suran7810)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and technical teams can use this skill to explore tradeoffs in a technical decision through a structured debate and receive summarized consensus, disagreement, and practical recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases such as "tech debate" may activate the skill unintentionally.

Mitigation: Confirm that the user wants a structured technical debate before continuing when the trigger is ambiguous.

Risk: Instruction-like content in debate topics or user interventions can influence the debate output.

Mitigation: Treat debate topics and interventions as debate content and avoid adding untrusted instruction-like text unless the user intends it to shape the output.

Risk: Debate outputs may present persuasive but incorrect or incomplete technical guidance.

Mitigation: Review the final consensus and recommendations against authoritative project requirements and technical sources before using them for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suran7810/skills/tech-debate)
- [Output format specification](artifact/references/output-format.md)
- [Role prompt templates](artifact/references/prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown conversation output with structured debate sections, role-labeled turns, judge summaries, user intervention prompts, and a final report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only skill; no code execution, external access, persistence, or credential handling according to security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
