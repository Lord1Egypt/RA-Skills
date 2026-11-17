## Description:

Use this skill whenever the user asks for a crossword puzzle: custom word/clue lists, themed crosswords, educational worksheets, or printable PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catorch](https://clawhub.ai/user/catorch)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, and puzzle creators use this skill to generate crossword puzzles from custom clues, themed word banks, or structured word lists. It guides an agent to use the local PuzzleTide CLI for valid interlocking grids, standard numbering, JSON output, and printable PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch and run an unpinned npm package if an agent uses the npx fallback automatically.

Mitigation: Prefer an already installed local PuzzleTide CLI, ask before any package install or download, and pin the package version when installing.

Risk: Running package commands in sensitive workspaces can introduce supply-chain exposure.

Mitigation: Avoid automatic npx execution in sensitive workspaces and review commands before execution.

## Reference(s):

- [PuzzleTide crossword](https://puzzletide.com/crossword)
- [Printable puzzles](https://puzzletide.com/printable)
- [PuzzleTide CLI source and docs](https://github.com/Caravaca-Labs/puzzletide-cli)
- [PuzzleTide npm package](https://www.npmjs.com/package/puzzletide)
- [PuzzleTide CLI reference](https://github.com/Caravaca-Labs/puzzletide-cli/blob/main/docs/cli.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline bash commands, JSON examples, and optional PDF or JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce printable crossword PDFs or structured JSON through the local PuzzleTide CLI.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
