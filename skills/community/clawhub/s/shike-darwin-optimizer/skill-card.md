## Description: <br>
Autonomous skill optimizer inspired by Karpathy's autoresearch that evaluates skill structure and effectiveness, proposes targeted improvements, validates with test prompts, and keeps or reverts changes through a git-based ratchet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sjj2026](https://clawhub.ai/user/sjj2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this agent skill to assess and improve other agent skills through structured scoring, test-prompt validation, human review checkpoints, and rollback of unsuccessful edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can evaluate and modify local skill files, including git commits or reverts. <br>
Mitigation: Use explicit targets, review proposed scope and diffs, and keep the human confirmation checkpoints before accepting changes. <br>
Risk: Static assets may load remote fonts, which can expose network metadata. <br>
Mitigation: Remove or block remote font loading in static assets when stricter privacy controls are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sjj2026/shike-darwin-optimizer) <br>
- [Andrej Karpathy autoresearch](https://github.com/karpathy/autoresearch) <br>
- [Skill README](README_EN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with scoring tables, diffs, JSON test prompts, TSV result records, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to SKILL.md, create test-prompts.json, update results.tsv, and request human confirmation before keeping changes.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
