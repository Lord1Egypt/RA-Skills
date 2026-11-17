## Description:

Skill Autogenesis helps tool-using agents summarize completed work, detect recurring workflows, and decide whether to create or patch a skill, store a memory note, or take no persistence action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn repeated, verified workflows into durable procedural memory. It helps decide whether a completed task should become a skill update, memory note, prompt guidance, or no-op.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to change skills, memory, prompts, or runtime behavior.

Mitigation: Configure the host to require approval before any skill-file, memory, prompt, or runtime-configuration write.

Risk: Past-session search can pull in broad or stale context.

Mitigation: Limit session-history searches to approved projects, time ranges, or explicitly relevant task scopes.

Risk: Untrusted repository text, web content, or tool output could be promoted into future agent instructions.

Mitigation: Review proposed procedural-memory changes before persistence and keep the hard stop rules active for preferences, policies, and one-off results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codeblackhole1024/skills/skill-autogenesis)
- [Source References](references/sources.md)
- [Classification Examples](references/classification-examples.md)
- [Hard Stop Rules](references/hard-stop-rules.md)
- [Hermes Agent Skill Creation Format](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/creating-skills.md)
- [Hermes Agent Skills Feature](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md)
- [Hermes Agent Prompt Guidance](https://github.com/NousResearch/hermes-agent/blob/main/agent/prompt_builder.py)
- [Hermes Agent Skill Manager Tool](https://github.com/NousResearch/hermes-agent/blob/main/tools/skill_manager_tool.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, classification records, skill-file drafts, patches, and supporting snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or modify procedural memory only after classification, recurrence, stability, and verification checks pass.]

## Skill Version(s):

1.3.2 (source: frontmatter, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
