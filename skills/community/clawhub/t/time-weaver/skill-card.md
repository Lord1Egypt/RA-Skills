## Description:

Time Weaver helps authors create choice-driven time-travel fiction by generating era settings, characters, scenes, chapters, branching choices, and publication/export artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harry720320](https://clawhub.ai/user/harry720320)

### License/Terms of Use:

MIT-0

## Use Case:

Authors and creative-writing agents use this skill to plan and write interactive Chinese time-travel novels with persistent world, character, and plot state. It can generate Markdown chapters, present reader choices, publish chapters to the Time Weaver website, and export manuscripts as EPUB files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated manuscript chapters may be uploaded to the Time Weaver website during the publishing workflow.

Mitigation: Review each chapter before publishing and avoid automatic publishing when content should remain private.

Risk: The publishing workflow stores a reusable API key in plaintext.

Mitigation: Do not paste unrelated secrets into chat, rotate exposed API keys, and harden local credential storage before production use.

Risk: Custom titles and imported chapter files are used by command-line publishing and EPUB export paths.

Mitigation: Treat custom titles and imported files as untrusted input until command and export paths are reviewed and hardened.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harry720320/skills/time-weaver)
- [Time Weaver Website](https://time-weaver-782300018128.us-west1.run.app/)
- [Character Generator Reference](references/character-generator.md)
- [Era Settings Reference](references/era-settings.md)
- [Maoni Style Guide](references/maoni-style.md)
- [Protagonist Templates Reference](references/protagonist-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown narrative text with inline command examples and generated manuscript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save book state under .learnings/books, publish chapters to a remote website, and export EPUB files through bundled Node.js scripts.]

## Skill Version(s):

0.7.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
