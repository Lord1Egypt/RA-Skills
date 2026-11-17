## Description:

Fetch Sudoku puzzles and store them as JSON in the workspace; render images on demand; reveal solutions later.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and puzzle creators use this skill to fetch Sudoku puzzles, save reusable puzzle JSON, render print-ready puzzle sheets, and reveal solutions when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A helper script can fetch arbitrary web URLs, which is broader than the documented sudokuonline.io workflow.

Mitigation: Prefer the documented sudoku.py preset commands and avoid invoking sudoku_fetcher.py with arbitrary URLs in restricted environments.

Risk: Commands write puzzle JSON and render artifacts into the workspace.

Mitigation: Run the skill only in workspaces where sudoku/puzzles/ and sudoku/renders/ outputs are expected, and review generated files before reuse.

## Reference(s):

- [Sudoku data format](references/DATA_FORMAT.md)
- [ClawHub Sudoku skill page](https://clawhub.ai/odrobnik/skills/sudoku)
- [Sudoku Online puzzle source](https://www.sudokuonline.io)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, guidance]

**Output Format:** [CLI output plus workspace files: JSON puzzle records, PNG/PDF/HTML renders, solution images, and share links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes puzzle and render files into the workspace and contacts external Sudoku or SudokuPad-related services when commands are invoked.]

## Skill Version(s):

2.6.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
