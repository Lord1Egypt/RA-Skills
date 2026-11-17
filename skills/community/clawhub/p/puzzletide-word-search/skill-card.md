## Description:

Generates themed or custom word search puzzles, printable worksheets, PDFs, SVGs, and JSON puzzle data with the local PuzzleTide CLI instead of hand-writing grids.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catorch](https://clawhub.ai/user/catorch)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, and developers use this skill to generate word search puzzles from custom word lists or bundled themes, including printable worksheets and structured puzzle data through the PuzzleTide CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends an unpinned npx fallback that can download and execute npm code before explicit approval.

Mitigation: Prefer an already-installed trusted ptide or puzzletide binary; remove or pin the npx fallback, or run it only after explicit approval in a sandboxed or lockfile-controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catorch/skills/puzzletide-word-search)
- [PuzzleTide word search](https://puzzletide.com/word-search)
- [Printable puzzles](https://puzzletide.com/printable)
- [Word search maker](https://puzzletide.com/maker)
- [PuzzleTide npm package](https://www.npmjs.com/package/puzzletide)
- [PuzzleTide CLI reference](https://github.com/Caravaca-Labs/puzzletide-cli/blob/main/docs/cli.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide the PuzzleTide CLI to produce PDF, SVG, or JSON puzzle outputs.]

## Skill Version(s):

0.1.1 (source: artifact/SKILL.md frontmatter and evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
