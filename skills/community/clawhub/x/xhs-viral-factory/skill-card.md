## Description:

XHS Viral Content Factory turns local source materials into Chinese Xiaohongshu draft posts, image prompt ideas, and tags using an OpenAI-compatible LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[less1001](https://clawhub.ai/user/less1001)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agents use this skill to analyze local notes or document folders and produce Xiaohongshu post drafts with style selection, image prompts, and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local files and optional posting history may be sent to the configured LLM provider.

Mitigation: Avoid pointing the source or history arguments at sensitive folders or files.

Risk: The LLM endpoint is configurable and the artifact does not enforce HTTPS or a trusted provider.

Mitigation: Set LLM_BASE_URL only to a trusted HTTPS provider endpoint before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/less1001/skills/xhs-viral-factory)
- [XHS Viral Factory Patterns](references/prompt_patterns.md)
- [XHS Viral Factory Detailed Installation and Usage](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text draft saved to a timestamped .txt file, plus terminal status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft content includes a title, body copy, image prompts, and tags.]

## Skill Version(s):

1.1.3 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
