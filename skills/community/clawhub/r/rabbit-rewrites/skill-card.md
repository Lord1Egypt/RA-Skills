## Description:

Rabbit Rewrites scans prose for flagged machine-writing patterns and can apply gated rewrites through a configured small local or OpenAI-compatible model endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whit3rabbit](https://clawhub.ai/user/whit3rabbit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and CI maintainers use this skill to plan, apply, and benchmark local-model rewrites of flagged prose while preserving facts and markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security review flags an under-disclosed Claude Code hook that can alter git commit and PR message text if registered.

Mitigation: Review before installing and do not register or enable scripts/claude_hook.py unless automatic Claude Code hook behavior is intentional.

Risk: Model-backed rewriting can send flagged passages to a configured OpenAI-compatible endpoint when --apply-model is used.

Mitigation: Use a local endpoint when privacy matters and review .rabbit-model plus RABBIT_MODEL_BASE_URL, RABBIT_MODEL_NAME, and RABBIT_MODEL_API_KEY before applying rewrites.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whit3rabbit/skills/rabbit-rewrites)
- [Models and Download Locations](references/models.md)
- [Security notes](SECURITY.md)
- [Qwen2.5 1.5B Instruct GGUF](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce rewrite plans or rewritten prose; applying model rewrites requires an explicitly configured OpenAI-compatible endpoint.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
