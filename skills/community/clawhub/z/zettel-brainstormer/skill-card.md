## Description: <br>
Build structured brainstorming notes from a seed zettel by retrieving linked notes, preprocessing each note with subagents for relevance extraction, drafting with cited evidence, and publishing a natural blog-style post with a final References section. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hxy9243](https://clawhub.ai/user/hxy9243) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, researchers, and developers use this skill to expand a local Obsidian or Zettelkasten seed note into a cited, publishable Markdown draft. The workflow retrieves related notes, filters them for relevance, synthesizes a traceable argument, and preserves a final references list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow reads notes from the configured zettel directory and may pass selected note content to drafting subagents. <br>
Mitigation: Keep zettel_dir scoped to notes intended for brainstorming and avoid configuring directories that contain private or unrelated material. <br>
Risk: Configuration includes local paths, retrieval limits, and model choices that affect what content is processed. <br>
Mitigation: Review config/models.json before use and confirm output_dir, zettel_dir, and agent model tiers match the intended workspace. <br>
Risk: Generated drafts can overstate relationships between weakly related notes or retain unsupported claims. <br>
Mitigation: Review inline citations and the final References section, and remove claims that are not clearly supported by the cited notes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hxy9243/zettel-brainstormer) <br>
- [Publisher Profile](https://clawhub.ai/user/hxy9243) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown article with YAML frontmatter, inline note citations, and a final References section; helper scripts also produce JSON candidate and draft-packet files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured local note directories, retrieval limits, and model tiers; final responses include the notes actually cited.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata and CHANGELOG, released 2026-03-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
