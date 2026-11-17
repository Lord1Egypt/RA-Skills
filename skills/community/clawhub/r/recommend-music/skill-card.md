## Description:

根据用户描述推荐2000年后经典热门歌曲的技能。当用户需要音乐推荐、寻找适合特定场景或情绪的音乐、或询问歌曲建议时使用此技能。技能结合情绪、场景、活动等多种因素，推荐真实存在且2000年后受欢迎的热门歌曲，提供详细的歌曲信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[flonerze](https://clawhub.ai/user/flonerze)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request music recommendations for moods, activities, scenes, genres, or broad listening ideas. The skill returns structured song suggestions with artist, album, year, genre, and a short reason for each recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is oriented toward Chinese music-recommendation prompts and may answer in Chinese by default.

Mitigation: Ask for the desired response language or have the agent adapt to the user's language preference.

Risk: Music metadata and popularity claims can be inaccurate if the agent relies only on memory.

Mitigation: For high-stakes or publication-quality use, verify song titles, artists, albums, years, and popularity claims against trusted music sources.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown recommendation list with song metadata and recommendation reasons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill normally recommends 5-10 real songs released in or after 2000 and may answer in Chinese unless the agent adapts language normally.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
