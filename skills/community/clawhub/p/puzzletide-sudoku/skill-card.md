## Description:

Use this skill whenever the user asks to generate, solve, or check a sudoku, including printable sheets, daily puzzles, difficulty-graded puzzles, or candidate solution verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catorch](https://clawhub.ai/user/catorch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent generate, solve, validate, and prepare Sudoku puzzles through the PuzzleTide CLI instead of relying on manual puzzle construction or hand-solving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to invoke an unpinned third-party npm package through npx, which may retrieve and execute package code at runtime.

Mitigation: Require explicit user approval before package retrieval or installation, and prefer a pinned, reviewed PuzzleTide package version before allowing execution.

Risk: The artifact claims local execution, but the security evidence flags that npx package retrieval may still require network access.

Mitigation: Check for an existing local ptide or puzzletide binary first, and treat any npx fallback as networked third-party code execution requiring approval.

## Reference(s):

- [PuzzleTide Sudoku](https://puzzletide.com/sudoku)
- [Printable PuzzleTide puzzles](https://puzzletide.com/printable)
- [PuzzleTide CLI source and docs](https://github.com/Caravaca-Labs/puzzletide-cli)
- [PuzzleTide CLI reference](https://github.com/Caravaca-Labs/puzzletide-cli/blob/main/docs/cli.md)
- [puzzletide npm package](https://www.npmjs.com/package/puzzletide)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash code blocks and optional generated puzzle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Sudoku grids, solutions, validation results, JSON CLI output, or printable PDF commands depending on the user request.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
