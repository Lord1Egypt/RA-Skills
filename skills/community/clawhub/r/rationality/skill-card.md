## Description:

Apply Critical Fallibilism to make decisions by testing ideas for decisive flaws, managing complexity, embracing criticism, and avoiding overreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xertrov](https://clawhub.ai/user/xertrov)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and other users apply this skill to structure high-stakes decisions, complex debugging, disagreement resolution, architecture evaluation, process improvement, and self-correction around explicit goals, context, constraints, and decisive criticisms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to save user corrections or refutations into long-term memory.

Mitigation: Install only in environments where memory writes require appropriate user consent, review, or platform-level controls.

Risk: The skill may lead an agent to run shell diagnostics after tool failures.

Mitigation: Use sandboxing, command approval, and least-privilege execution controls before allowing shell commands.

Risk: The skill may lead an agent to reset git state without enough safeguards.

Mitigation: Require explicit user approval and repository state review before destructive git operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xertrov/skills/rationality)
- [Critical Fallibilism Forum](https://discuss.criticalfallibilism.com/)
- [Ember's Blog](https://ember.vecnet.ai)
- [Theory of Constraints](https://en.wikipedia.org/wiki/Theory_of_constraints)
- [Karl Popper's Falsifiability](https://en.wikipedia.org/wiki/Falsifiability)
- [frameworks/decision.md](frameworks/decision.md)
- [frameworks/paths-forward.md](frameworks/paths-forward.md)
- [frameworks/self-correction.md](frameworks/self-correction.md)
- [frameworks/translation.md](frameworks/translation.md)
- [templates/igc-evaluation.md](templates/igc-evaluation.md)
- [templates/checklist.md](templates/checklist.md)
- [templates/debate-tree.md](templates/debate-tree.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance, checklists, and structured decision templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose reasoning frameworks, binary evaluations, refutations, checklists, and operational next steps.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
