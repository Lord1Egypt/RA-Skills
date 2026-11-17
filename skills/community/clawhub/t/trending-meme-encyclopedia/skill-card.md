## Description:

获取B站、抖音等平台当天的热门梗/迷因，追溯热梗来源、解释含义、整理相关视频素材，生成结构化的热梗百科文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hwl1413520](https://clawhub.ai/user/hwl1413520)

### License/Terms of Use:

MIT-0

## Use Case:

Content researchers, creators, and social media analysts use this skill to identify current Chinese internet memes, trace their sources, explain meanings, collect related media links, and produce structured encyclopedia-style documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer has unsafe path handling that could execute unintended Python code if a crafted install path is used.

Mitigation: Review install.sh before running it, prefer manual installation or the default detected skills directory from a trusted local path, and do not pass an install path supplied by someone else.

Risk: Trending meme research depends on fast-changing public platform results and may produce stale or weakly sourced explanations.

Mitigation: Record the collection time, cite source links where available, and verify meme origins before using the output in published work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hwl1413520/skills/trending-meme-encyclopedia)
- [热梗类型分类详解](artifact/references/MEME_TYPES.md)
- [来源追溯技巧](artifact/references/SOURCE_TRACING.md)
- [百科模板](artifact/assets/encyclopedia_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown encyclopedia entries, research summaries, source-tracing notes, JSON exports, and optional shell or Python helper commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require web access to current platform results; outputs should cite collection time and source links where available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
