## Description:

Auto-enrich Bear research notes tagged 「待整理」 with topic-matched GIFs by reading notes via grizzly, searching GIFs via gifgrep or Tenor, appending media, and removing the tag.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Bear power users use this skill to batch-process research notes that are tagged for cleanup, add a relevant supporting GIF, and report notes that could not be enriched.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can batch-edit Bear notes and may overwrite note content while removing the cleanup tag.

Mitigation: Back up Bear notes first, review the tagged note set before execution, and prefer controlled step-by-step runs for important notes.

Risk: Title-derived search terms may be sent to an external GIF search service.

Mitigation: Run only when this external data flow is acceptable, and avoid processing notes whose titles or findings contain sensitive information.

Risk: The release evidence flags the package as suspicious because user control and disclosure around note rewriting and external GIF search are limited.

Mitigation: Review the skill before installing, use an explicitly approved grizzly dependency, and require opt-in network behavior for GIF lookup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/research-gif-enricher)
- [grizzly Go module](https://github.com/tylerwince/grizzly)
- [Packaged skill definition](artifact/SKILL.md)
- [Packaged batch processing script](artifact/scripts/process_tagged.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown note additions, shell commands, and a concise processing report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update Bear note contents by appending media links and removing the cleanup tag.]

## Skill Version(s):

0.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
