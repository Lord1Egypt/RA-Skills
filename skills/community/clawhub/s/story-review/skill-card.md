## Description: <br>
Story Review coordinates multi-perspective fiction review, using deployed reviewer agents when available and falling back to solo review when agents or reference files are unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External writers, editors, and writing teams use this skill to review Chinese web-fiction drafts for structure, character behavior, prose quality, continuity, platform fit, and concrete revision actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full and lean review modes may read local story files and share scoped excerpts or file paths with local reviewer agents. <br>
Mitigation: Use solo mode or specify a narrow review scope when tighter control over file access and excerpt sharing is needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/worldwonderer/skills/story-review) <br>
- [OpenClaw Source](https://github.com/worldwonderer/oh-story-claudecode) <br>
- [Anti-AI Writing Guide](references/anti-ai-writing.md) <br>
- [Banned Words and Sentence Patterns](references/banned-words.md) <br>
- [Character Relations and Romance Guide](references/character-relations.md) <br>
- [Dialogue Design Guide](references/dialogue-mastery.md) <br>
- [Plot Core Methods](references/plot-core-methods.md) <br>
- [Web Fiction Quality Checklist](references/quality-checklist.md) <br>
- [Generic Web Fiction Review Rubric](references/quality-rubric.md) <br>
- [Fanqie Novel Quality Rubric](references/rubrics/fanqie.md) <br>
- [Qidian Quality Rubric](references/rubrics/qidian.md) <br>
- [Zhihu Yanxuan Story Quality Rubric](references/rubrics/zhihu.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with structured findings and review metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports requested mode, effective mode, fallback status, rubric source, reviewer status, prioritized findings, and a revision action plan.] <br>

## Skill Version(s): <br>
1.1.10 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
