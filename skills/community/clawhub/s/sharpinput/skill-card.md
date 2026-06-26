## Description: <br>
SharpInput improves prompts, questions, requirements, plans, ideas, and messages into clearer, better scoped, copy-ready inputs while preserving the user's intent and avoiding direct answers to the underlying task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoyechen](https://clawhub.ai/user/gaoyechen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use SharpInput to turn weak or ambiguous prompts, questions, and ideas into clearer, better scoped, copy-ready prompts for use with AI systems or people. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save and silently reuse detailed user preference history. <br>
Mitigation: Clear included preference files before installation and require opt-in before any self-learning writes. <br>
Risk: The skill requests broader file and command permissions than its prompt-improvement workflow clearly needs. <br>
Mitigation: Review requested permissions before installation, remove Bash where possible, and constrain Write access to the preference JSON when retained. <br>
Risk: Silent autofill from stored preferences can affect future prompt upgrades without the user's awareness. <br>
Mitigation: Require confirmation before reusing stored preference values in each session. <br>


## Reference(s): <br>
- [ClawHub SharpInput release page](https://clawhub.ai/gaoyechen/sharpinput) <br>
- [Handoff contract](artifact/references/handoff-contract.md) <br>
- [Intent taxonomy](artifact/references/intent-taxonomy.md) <br>
- [Prompt patterns](artifact/references/prompt-patterns.md) <br>
- [Pressure strategies](artifact/references/pressure-strategies.md) <br>
- [Output templates](artifact/references/output-templates.md) <br>
- [Judge rubric](artifact/references/judge-rubric.md) <br>
- [Self-learning reference](artifact/references/self-learning.md) <br>
- [User preferences reference](artifact/references/user-preferences.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with structured sections and a quote block containing a copy-ready upgraded prompt] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask concise clarification questions before producing the final prompt; does not answer the underlying task by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter declares 3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
