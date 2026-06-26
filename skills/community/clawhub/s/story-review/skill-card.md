## Description: <br>
Story Review coordinates adversarial, multi-perspective review of Chinese web-fiction drafts, using deployed reviewer agents when available and falling back to a built-in rubric when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authors, editors, and writing teams use this skill to review draft fiction for structure, character motivation, prose quality, continuity, platform fit, and concrete revision actions. It is especially focused on Chinese web-fiction workflows and platform-specific rubrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect draft fiction, planning files, and related project context. <br>
Mitigation: Run it only in workspaces whose writing material may be reviewed by the active agent, and provide explicit file scopes when possible. <br>
Risk: The punctuation normalizer can modify files when run without --check. <br>
Mitigation: Use --check for review-only runs, and run write mode only after deciding that punctuation normalization is desired. <br>
Risk: Full and lean modes may call deployed reviewer agents when the environment supports agent spawning. <br>
Mitigation: Confirm the deployed reviewer agents are trusted and current; otherwise use solo mode or rely on the skill's fallback behavior. <br>


## Reference(s): <br>
- [Story Review ClawHub page](https://clawhub.ai/worldwonderer/skills/story-review) <br>
- [OpenClaw source metadata](https://github.com/worldwonderer/oh-story-claudecode) <br>
- [Quality checklist](references/quality-checklist.md) <br>
- [Quality rubric](references/quality-rubric.md) <br>
- [Anti-AI writing guide](references/anti-ai-writing.md) <br>
- [Banned words and phrases](references/banned-words.md) <br>
- [Plot core methods](references/plot-core-methods.md) <br>
- [Character relations](references/character-relations.md) <br>
- [Dialogue mastery](references/dialogue-mastery.md) <br>
- [Fanqie rubric](references/rubrics/fanqie.md) <br>
- [Qidian rubric](references/rubrics/qidian.md) <br>
- [Zhihu rubric](references/rubrics/zhihu.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review report with structured findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include requested and effective review mode, fallback status, rubric source, severity-tagged findings, and concrete revision guidance.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
