## Description: <br>
Roundtable Pai turns a user's question into a three-person roundtable discussion using fictionalized public-figure-style personas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouxiang1](https://clawhub.ai/user/zhouxiang1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to explore decisions, trends, execution plans, reflection questions, and creative ideas through a structured simulated roundtable. The skill helps an agent run one discussion step at a time, select three personas, collect user input between rounds, and synthesize a final conclusion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fictionalized public-figure personas may be mistaken for real endorsements, current statements, or authoritative personal advice. <br>
Mitigation: Present persona voices as simulations based on public material and keep the documented disclaimer visible before the first discussion round. <br>
Risk: The roundtable may discuss high-impact medical, legal, financial, crypto, purchase, self-harm, violence, or illegal-action topics. <br>
Mitigation: Reduce advice strength for high-risk topics, avoid directly actionable harmful steps, and direct users to independent verification or appropriate professional support. <br>
Risk: User text is passed through a controller workflow, so unsafe shell handling could turn ordinary input into execution risk. <br>
Mitigation: Use the documented stdin-only invocation pattern and treat user text as data, not executable shell or Python code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouxiang1/roundtable-pai) <br>
- [README](artifact/README.md) <br>
- [Safety](artifact/references/safety.md) <br>
- [Interface Contracts](artifact/references/interface-contracts.md) <br>
- [User-Facing Output](artifact/references/user-facing-output.md) <br>
- [Discussion Quality](artifact/references/discussion-quality.md) <br>
- [Candidate Selection](artifact/references/candidate-selection.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text conversation turns with candidate lists, one-round discussion responses, user choice prompts, and final conclusion fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill advances one discussion state per user turn and includes a persona-simulation disclaimer before the first discussion round.] <br>

## Skill Version(s): <br>
1.6.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
