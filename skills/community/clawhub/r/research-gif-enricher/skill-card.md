## Description: <br>
Auto-enrich Bear research notes tagged 「待整理」 with topic-matched GIFs by reading notes via grizzly, searching GIFs, appending media, and removing the tag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Bear users and research-note maintainers use this skill to batch-process notes tagged 「待整理」, add relevant GIF media, and clear the organizing tag after processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can batch rewrite private Bear notes without a built-in preview or rollback. <br>
Mitigation: Back up or export the affected Bear notes first, review the tagged notes, and use a dry-run or confirmation step before allowing writes. <br>
Risk: Note-derived search terms may be sent to an external GIF service. <br>
Mitigation: Run only on notes whose titles or keywords are acceptable to share externally, and review or redact search terms before lookup when notes may contain sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/research-gif-enricher) <br>
- [grizzly Bear CLI](https://github.com/tylerwince/grizzly) <br>
- [Tenor GIF search API](https://tenor.googleapis.com/v2/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and Markdown image snippets for Bear notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append a Supporting Media section to Bear notes and remove the target tag.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
