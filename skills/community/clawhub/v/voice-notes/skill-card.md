## Description:

Organize voice message transcripts into a structured, searchable knowledge base with tags, links, and progressive note-taking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn platform-transcribed voice messages into local Markdown transcripts, organized notes, tag registries, indexes, and wiki-style links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw transcribed voice messages are retained as local Markdown files under ~/voice-notes/.

Mitigation: Avoid highly sensitive recordings unless local retention is acceptable, and manage filesystem access, backups, and cleanup policies for ~/voice-notes/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/voice-notes)
- [Voice Notes skill definition](artifact/SKILL.md)
- [Memory setup](artifact/memory-template.md)
- [Note processing](artifact/processing.md)
- [Linking system](artifact/linking.md)
- [Tag management](artifact/tags.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown notes, transcript files, index entries, tag registry updates, wiki-style links, and occasional shell setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores transcript text and processed notes locally under ~/voice-notes/; supports linux, darwin, and win32; no required binaries.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
