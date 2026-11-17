## Description:

Skill Creator helps agents create, update, evaluate, improve, and manage skills across agent platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hulk-yin](https://clawhub.ai/user/hulk-yin)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to turn intent into skill files, run qualitative and quantitative evaluation loops, improve skill triggering, and package or distribute skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled evaluation viewer can mishandle untrusted evaluation files.

Mitigation: Review or patch the viewer's HTML embedding and rendering paths before using it on untrusted outputs, and keep evaluation workspaces isolated.

Risk: The bundled viewer can stop other local applications when it starts.

Mitigation: Check for an unused port before launching the viewer, avoid elevated privileges, and do not run it in shared environments without operator awareness.

Risk: Description optimization may send skill or evaluation content to Anthropic.

Mitigation: Avoid running description optimization on sensitive or confidential skill content unless external processing is approved.

## Reference(s):

- [Skill Creator schemas](artifact/references/schemas.md)
- [Skill Manager](https://github.com/ZiweiAxis/skill-manager)
- [ClawHub Skill Creator release](https://clawhub.ai/hulk-yin/skills/skill-creator-usm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, code, configuration, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or revise skill files and evaluation artifacts when used by an agent with filesystem access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
