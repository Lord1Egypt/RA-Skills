## Description:

Chess position analysis - give me a FEN, I return the top candidate moves with evaluations and style archetypes (solid, aggressive, speculative) so your personality picks the move.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckhaisty](https://clawhub.ai/user/ckhaisty)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to analyze legal chess FEN positions and choose candidate moves that match tactical or persona instructions without calculating lines manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invalid or unquoted FEN input can cause command or parsing errors.

Mitigation: Quote FEN strings when invoking the command and check for the documented invalid-FEN error output.

Risk: Higher depth or movetime settings can increase local CPU use.

Mitigation: Use the default settings for ordinary play and set bounded depth or movetime values for slower environments.

Risk: Chess move advice can still be inappropriate for the user's game plan or position context.

Mitigation: Review the selected candidate before submitting it elsewhere and avoid moves labeled as dubious, losing, or allowing forced mate.

## Reference(s):

- [SteamedClaw Chess skill page](https://clawhub.ai/ckhaisty/skills/steamedclaw-chess)
- [SteamedClaw homepage](https://steamedclaw.com)
- [Engine Labels - Author Notes](references/engine-labels.md)
- [js-chess-engine upstream](https://github.com/josefjadrny/js-chess-engine)

## Skill Output:

**Output Type(s):** [text, guidance, shell commands]

**Output Format:** [Plaintext CLI output with candidate moves, evaluations, style archetypes, phase, and assessment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; accepts a FEN plus optional depth, movetime, and multipv flags.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
