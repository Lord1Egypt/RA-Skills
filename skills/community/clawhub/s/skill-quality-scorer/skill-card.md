## Description: <br>
Deterministic TRACE+ quality scorer for Agent Skills that runs a bundled static audit first, applies a six-dimension 30-item rubric, and outputs JSON plus Markdown review reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris1wang3](https://clawhub.ai/user/chris1wang3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to score, audit, compare, and batch-review Agent Skill directories before publication or iteration. It is intended as an advisory quality review aid, not a replacement for behavioral testing or human security review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local skill directories and linked files during scoring. <br>
Mitigation: Run it only on directories intentionally selected for review and avoid unrelated private workspaces. <br>
Risk: Static quality scores may be mistaken for complete behavioral or security assurance. <br>
Mitigation: Treat the output as advisory and supplement it with behavioral tests and human security review before relying on the score. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chris1wang3/skill-quality-scorer) <br>
- [Scoring Engine Deterministic](references/scoring-engine-deterministic.md) <br>
- [Audit Playbook](references/audit-playbook.md) <br>
- [Sample Score v2](examples/sample-score-v2.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [JSON and Markdown review reports with scoring tables, evidence, trigger tests, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-skill, comparison, and batch scoring modes use the same TRACE+ v2 rubric and formula.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
