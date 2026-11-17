## Description:

Automates long-form technical proposal writing with multi-agent chapter generation, checkpointed continuation, and persistent progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deardavidzheng](https://clawhub.ai/user/deardavidzheng)

### License/Terms of Use:

MIT-0

## Use Case:

External teams and developers use this skill to generate technical proposal documents from project requirements, outlines, and reference material. It is intended for large proposal workflows that benefit from chapter-level progress tracking and continuation across agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent continuation can keep scanning projects and starting follow-up agent work without clear per-run control.

Mitigation: Keep cron and heartbeat continuation disabled by default, limit operation to named project directories, and document how to pause automation and remove cron entries.

Risk: Generated proposals can include incorrect or misleading content if outputs are accepted without review.

Mitigation: Review generated chapters, final.md, CONTINUE.md, and progress.json before relying on or publishing the proposal.

Risk: Reference files or authenticated URLs may expose sensitive content to spawned sessions.

Mitigation: Avoid sensitive reference files and authenticated URLs unless the project owner has approved their use for proposal generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deardavidzheng/skills/tech-proposal-autopilot)
- [README](artifact/README.md)
- [Guide](artifact/GUIDE.md)
- [Quick Reference](artifact/QUICKREF.md)
- [Migration Guide](artifact/MIGRATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown proposal files with JSON progress files and shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates chapter files, final proposal Markdown, progress.json, CONTINUE.md, logs, and continuation trigger files when automation is enabled.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
