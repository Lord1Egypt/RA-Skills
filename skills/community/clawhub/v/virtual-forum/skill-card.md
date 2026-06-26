## Description: <br>
Virtual Forum orchestrates structured multi-agent debates between distilled persona skills and can add game-theory and behavioral-economics analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erongcao](https://clawhub.ai/user/erongcao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run structured debates, roundtable discussions, adversarial decision sessions, and strategy analysis across persona skills. It is intended for exploratory analysis and decision support rather than authoritative conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bash workflow can read local Skill files and send their contents plus discussion history to Claude. <br>
Mitigation: Review Skill files for secrets before use, set SKILLS_DIR and OUTPUT_DIR deliberately, and run the workflow only when external API transfer is acceptable. <br>
Risk: Parallel Claude CLI calls can consume API quota and require valid local Claude CLI credentials. <br>
Mitigation: Confirm authentication, quota, and cost expectations before running long or multi-participant debates. <br>
Risk: Game-theory and behavioral-economics outputs may be persuasive or experimental rather than neutral analysis. <br>
Mitigation: Treat debate outcomes and strategy advice as decision-support material and apply independent human review before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erongcao/virtual-forum) <br>
- [README](artifact/README.md) <br>
- [Usage guide](artifact/USAGE.md) <br>
- [Claude Code parallel debate script documentation](artifact/v5/README.md) <br>
- [Game-theory module documentation](artifact/v5/game-theory/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown debate transcripts and reports, JavaScript return objects, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce debate records, moderator summaries, decision reports, game-theory analysis, and behavioral-economics strategy guidance.] <br>

## Skill Version(s): <br>
5.0.3 (source: server release evidence, package.json, and CHANGELOG; SKILL.md frontmatter says 5.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
