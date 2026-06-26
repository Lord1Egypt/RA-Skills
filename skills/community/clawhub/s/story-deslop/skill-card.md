## Description: <br>
Story Deslop detects and reduces AI-like patterns in Chinese web fiction so drafts read more natural and less templated. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External writers, editors, and agent users can use this skill to inspect Chinese web fiction drafts for AI-like prose patterns, produce a concise issue report, rewrite marked passages, and normalize punctuation while preserving story intent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases can cause an agent to rewrite or normalize drafts unexpectedly. <br>
Mitigation: Ask for preview or diff behavior before applying changes to files, and keep backups for drafts that matter. <br>
Risk: Style cleanup can accidentally remove story hooks, character details, or plot-relevant phrasing. <br>
Mitigation: Review the rewritten output against the original and enforce the skill's deletion limits and preservation rules. <br>


## Reference(s): <br>
- [Story Deslop ClawHub Page](https://clawhub.ai/worldwonderer/skills/story-deslop) <br>
- [OpenClaw Source Metadata](https://github.com/worldwonderer/oh-story-claudecode) <br>
- [Anti-AI Writing Guide](references/anti-ai-writing.md) <br>
- [Banned Words and Pattern Table](references/banned-words.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with revised Chinese prose and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May edit local text files when asked; reports character-change and deletion-risk information for review.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
