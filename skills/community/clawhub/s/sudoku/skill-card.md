## Description: <br>
Fetch Sudoku puzzles and store them as JSON in the workspace; render images on demand; reveal solutions later. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and puzzle creators use this skill to fetch Sudoku puzzles, store reusable puzzle JSON, render printable or viewable boards, and reveal full or partial solutions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external Sudoku puzzle sites to fetch puzzle data. <br>
Mitigation: Run it only where outbound access to those puzzle sources is acceptable, and review fetched content before sharing or relying on it. <br>
Risk: The skill creates local puzzle files, renders, solutions, and share links in the workspace. <br>
Mitigation: Use a workspace appropriate for saved puzzle answers and avoid sharing saved files when solutions should remain private. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/odrobnik/sudoku) <br>
- [Sudoku Data Format](references/DATA_FORMAT.md) <br>
- [SudokuOnline puzzle source](https://www.sudokuonline.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [JSON responses, Markdown links, and workspace files such as JSON, PNG, PDF, or HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates workspace-local puzzle and render files under sudoku/puzzles/ and sudoku/renders/; may contact Sudoku puzzle sites to fetch puzzles.] <br>

## Skill Version(s): <br>
2.6.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
