## Description: <br>
Meta-skill that helps an agent combine installed skills, record useful combinations, and produce recurring operational summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and OpenClaw operators use this skill to identify useful combinations among installed skills, maintain a catalogue of proven patterns, and receive weekly summaries of discovered capabilities and skill gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly coordinates other installed skills, which can amplify downstream actions if approval boundaries are unclear. <br>
Mitigation: Define explicit approval rules for trades, deployments, public posts, account changes, and other irreversible actions before enabling the skill. <br>
Risk: The skill writes persistent operational memory that may accumulate inaccurate, stale, or sensitive summaries if left unreviewed. <br>
Mitigation: Review COMBINATIONS.md, .learnings entries, and dated memory summaries regularly, and keep entries limited to non-sensitive metadata. <br>
Risk: Weekly reports are sent through a configured Telegram notification channel. <br>
Mitigation: Limit Telegram reports to non-sensitive summaries and keep notification credentials in environment variables only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/georges91560/skill-combinator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown catalogue entries, learning logs, weekly reports, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes operational memory files such as COMBINATIONS.md, .learnings entries, and dated run summaries; weekly reports may be delivered through the configured Telegram notification channel.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
