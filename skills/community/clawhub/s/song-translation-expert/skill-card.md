## Description:

Song Translation Expert helps agents translate song lyrics to or from Chinese with line-aligned text, singability, rhyme, cultural notes, genre conventions, and optional structured outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sakurakilove](https://clawhub.ai/user/sakurakilove)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to translate, explain, align, annotate, and localize song lyrics across major music genres, especially into Chinese or from Chinese. It is suited for line-by-line lyric translation, bilingual comparison, singable rewrites, and culture-aware notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Song-name or URL requests may require web lookup for source lyrics or reference translations.

Mitigation: Use web lookup only when needed, cite or explain the source basis when possible, and review retrieved lyrics before translating.

Risk: File export requests may create persistent local copies of lyrics.

Mitigation: Prefer chat-only output unless the user explicitly requests saved files, and make saved-file behavior clear.

Risk: AI-generated lyric translation may be inaccurate for rare languages, dialects, older language forms, cultural references, or publication-grade use.

Mitigation: Use the built-in quality checklist and recommend human review for high-stakes, public, or professional publication contexts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sakurakilove/skills/song-translation-expert)
- [Translation Principles](references/translation_principles.md)
- [Special Elements Handling](references/special_elements.md)
- [Output Formats](references/output_formats.md)
- [Quality Checklist](references/quality_checklist.md)
- [Japanese Songs Guide](references/japanese_songs.md)
- [English Songs Guide](references/english_songs.md)
- [World Songs Guide](references/world_songs.md)
- [Sample Corpus](assets/sample_corpus.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown lyric translations by default; may also produce JSON, Markdown tables, LRC-style text, or file-generation guidance when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Line-aligned bilingual output with optional translation notes, quality checks, and helper-script commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
