## Description: <br>
Helps an agent identify user-approved opportunities to persist preferences, improve skills, and update global behavior rules through a three-layer self-evolution workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sjj2026](https://clawhub.ai/user/sjj2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to help an agent capture durable user preferences, repeated failure lessons, and high-impact behavior rules after explicit review and approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose persistent changes to memory, skill instructions, global rules, Git history, and notifications to other bots. <br>
Mitigation: Review every target file, proposed diff, commit, rollback, and notification before approval, with extra scrutiny for SKILL.md and CLAUDE.md changes. <br>
Risk: Self-evolution can preserve sensitive information or short-term preferences as durable behavior. <br>
Mitigation: Avoid approving secrets, credentials, personal data, temporary emotional states, or ambiguous preferences; ask for clarification when intent is unclear. <br>


## Reference(s): <br>
- [Self-Evolve Skill on ClawHub](https://clawhub.ai/sjj2026/shike-self-evolve) <br>
- [AutoClaw self-evolution concept](https://autoglm.zhipuai.cn/autoclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown request cards with optional inline shell commands and file-change guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent memory, skill, global-rule, Git, and notification changes that require user review before execution.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
