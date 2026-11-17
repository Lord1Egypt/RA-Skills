## Description:

Use this skill when the user wants printable puzzle worksheets, including print-ready word search, crossword, and sudoku PDFs with solution pages produced through the local PuzzleTide CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catorch](https://clawhub.ai/user/catorch)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, activity-book creators, and agents acting for them use this skill to generate printable puzzle worksheets and packets from local CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned `npx puzzletide --version` fallback can download and execute npm package code.

Mitigation: Prefer an already-installed `ptide` or `puzzletide` binary; ask before installing or using npx, and pin the npm package version when a download is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catorch/skills/puzzletide-printable-puzzles)
- [PuzzleTide printable puzzles](https://puzzletide.com/printable)
- [puzzletide npm package](https://www.npmjs.com/package/puzzletide)
- [PuzzleTide CLI reference](https://github.com/Caravaca-Labs/puzzletide-cli/blob/main/docs/cli.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with inline shell commands; generated CLI artifacts are PDF or SVG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The PuzzleTide CLI can produce local printable puzzle PDFs with solution pages, or SVG files for embedding.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
