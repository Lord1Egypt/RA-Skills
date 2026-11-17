## Description:

Guides agents through structured StoryForge storytelling workflows to draft, validate, and hand off candidate narrative artifacts as files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taosiuman](https://clawhub.ai/user/taosiuman)

### License/Terms of Use:

MIT

## Use Case:

Writers, editors, and creative teams use this skill to guide an agent in preparing structured novels, scripts, character profiles, interactive stories, comics, and motion-drama materials. The agent creates candidate project files for human review rather than adopting them into a live application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may create or update files in the selected project directory.

Mitigation: Review the target directory and proposed writes before allowing file changes.

Risk: Generated creative details or field mappings may be inaccurate or mistaken for approved canon.

Mitigation: Validate candidate files and source evidence, then require the author to review and explicitly accept them.

Risk: Optional media-production integration notes may not fit the local environment.

Mitigation: Use those integrations only when explicitly requested and configured for the project.

## Reference(s):

- [StoryForge writing skill release](https://clawhub.ai/taosiuman/skills/storyforge-writing)
- [StoryForge upstream data-contract reference](https://github.com/yuanbw2025/storyforge)
- [Data envelope and file-delivery contract](artifact/contracts/S-data-envelope.md)
- [Writable field registry](artifact/references/field-registry.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance, Shell commands]

**Output Format:** [Project-local narrative Markdown and structured JSON files with validation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidate artifacts require author review before adoption; supporting files record source selection and validation evidence.]

## Skill Version(s):

0.5.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
