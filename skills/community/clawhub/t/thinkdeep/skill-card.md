## Description:

Structured reasoning protocol for Claude that prompts step-by-step analysis, self-critique, and confidence scoring before answering complex questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and other agent users can use this skill to structure analysis for complex technical questions, trade-off decisions, code review, risk assessment, and root-cause analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make responses more verbose or slower for prompts where deep analysis is unnecessary.

Mitigation: Use it for complex decisions, debugging, reviews, risk analysis, and other high-cost answers; skip it for simple transformations or obvious factual answers.

Risk: Broad activation keywords may cause the reasoning protocol to run more often than intended.

Mitigation: Review activation behavior after installation and narrow trigger terms if the skill activates on routine prompts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiajiaoy/skills/thinkdeep)
- [ClawHub Homepage Metadata](https://clawhub.ai/skills/thinkdeep)
- [Publisher Profile](https://clawhub.ai/user/jiajiaoy)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text with an optional structured thinking block followed by an answer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only skill; no files, credentials, network access, or tool execution are requested by the artifact.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence; artifact frontmatter shows 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
