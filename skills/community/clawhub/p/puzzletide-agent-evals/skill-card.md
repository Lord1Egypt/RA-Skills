## Description:

Use this skill when the user wants verifiable reasoning tasks to benchmark or test an LLM or agent: reproducible puzzle task sets such as sudoku and word search with objective, by-construction grading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catorch](https://clawhub.ai/user/catorch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluation engineers use this skill to generate reproducible local puzzle benchmarks, run models or agents against those tasks, and grade answers deterministically without an LLM judge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned npx availability check can fetch and execute third-party npm code.

Mitigation: Prefer an already installed local ptide or puzzletide binary; use a pinned, reviewed package version and explicit user approval before npm or npx execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catorch/skills/puzzletide-agent-evals)
- [Skill homepage](https://github.com/Caravaca-Labs/puzzletide-cli/blob/main/docs/agent-skills.md#puzzletide-agent-evals)
- [PuzzleTide CLI repository](https://github.com/Caravaca-Labs/puzzletide-cli)
- [PuzzleTide npm package](https://www.npmjs.com/package/puzzletide)
- [PuzzleTide CLI reference](https://github.com/Caravaca-Labs/puzzletide-cli/blob/main/docs/cli.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON task or grading files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates deterministic local puzzle task sets and grading summaries when used with the PuzzleTide CLI.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
