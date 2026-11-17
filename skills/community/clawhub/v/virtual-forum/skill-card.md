## Description:

虚拟论坛 orchestrates structured multi-agent debates between distilled persona skills and can add game-theory analysis for strategic discussions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erongcao](https://clawhub.ai/user/erongcao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run structured discussions, adversarial debates, and decision-oriented forums among persona skills. It can produce debate transcripts, summaries, decisions, and strategy-oriented game-theory analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local Skill files and debate prompts can be sent to the Claude provider through the user's local Claude Code setup.

Mitigation: Review participant Skill files for secrets or private instructions before use, and avoid including sensitive skills in debate sessions.

Risk: The debate script has weak scoping controls around which local skills may be read.

Mitigation: Run the skill only in a contained workspace with explicit participant selection and narrow SKILLS_DIR and OUTPUT_DIR values.

Risk: Broad or casual activation may expose private context without clear user consent.

Mitigation: Use explicit activation and obtain consent before sending persona skill content or debate prompts to external model processes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erongcao/skills/virtual-forum)
- [README.md](artifact/README.md)
- [USAGE.md](artifact/USAGE.md)
- [v5 Claude Code parallel debate README](artifact/v5/README.md)
- [v5 game-theory README](artifact/v5/game-theory/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, plain text, JavaScript examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include debate transcripts, round summaries, decision recommendations, and game-theory reports.]

## Skill Version(s):

5.0.3 (source: release evidence, package.json, CHANGELOG, released 2026-04-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
