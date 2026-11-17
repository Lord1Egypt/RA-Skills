## Description:

Smart Prompt Builder generates structured writing prompts for fiction scenes using corpus results, scene context, and optional voice profile settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writing-agent users use this skill to build reusable prompts for fiction description, dialogue, action, and emotion scenes. It can incorporate scene context, character state, retrieved corpus excerpts, and style preferences before passing the prompt to a downstream writer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled LLM script can send writing context and style files to Aliyun DashScope.

Mitigation: Use the local build_prompt.py path for local-only prompt construction, and run build_prompt_llm.py only with data intended for that provider.

Risk: Private manuscripts, personal data, proprietary style guides, or secrets may be exposed if provided to the LLM variant.

Mitigation: Review inputs before execution and avoid passing sensitive or confidential material to build_prompt_llm.py.

Risk: Dependencies are not fully pinned for sensitive environments.

Mitigation: Review and pin dependencies before installing or deploying this skill in controlled environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuzhihui886/skills/smart-prompt-builder)
- [Publisher Profile](https://clawhub.ai/user/yuzhihui886)
- [Skill README](artifact/SKILL.md)
- [Script README](artifact/scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON prompt structures, with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local prompt builder can export plain text; bundled LLM variant can write JSON prompt data.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
