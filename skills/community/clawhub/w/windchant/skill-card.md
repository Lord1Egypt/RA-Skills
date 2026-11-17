## Description:

风咏将古诗词、古文名篇、现代散文或小说改编为歌曲，输出带原文化用出处的歌词、曲风和编曲方案，以及可用于 AI 音乐工具的提示。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to adapt Chinese literary works or prose into song lyrics with narrative structure, source-text attribution, and music direction. It is also useful for teaching how source text is transformed into lyrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad Chinese songwriting requests and tends to produce Chinese-formatted responses.

Mitigation: Use it for Chinese literary songwriting workflows, and choose a different skill or add explicit instructions when multilingual output or source-text-only adaptation is required.

Risk: Literary background or authorship claims can be uncertain when the user supplies only a title or ambiguous source material.

Mitigation: Use reliable sources for source text and background, mark uncertain research as tentative, and review factual notes before using outputs in teaching or publication.

Risk: Song outputs can overuse direct quotations or accidentally copy existing lyrics if prompts introduce copyrighted song examples.

Mitigation: Limit direct source-text quotation as documented by the skill, avoid reusing third-party lyrics, and review generated lyrics for originality before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/windchant)
- [Skill workflow](artifact/SKILL.md)
- [Analysis and textual research module](artifact/modules/01-analyze.md)
- [Lyrics methodology module](artifact/modules/02-lyrics.md)
- [Music arrangement module](artifact/modules/03-music.md)
- [Output format module](artifact/modules/04-output.md)
- [Textual melody description module](artifact/modules/05-score.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured Chinese sections for analysis, narrative outline, lyrics, music direction, AI music prompts, and source-text comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only output; no executable code, persistence, external tools, or sensitive access are part of the skill evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
