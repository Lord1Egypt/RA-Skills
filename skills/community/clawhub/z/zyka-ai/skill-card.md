## Description:

Generate AI videos, images, voice, and AI app outputs using the Zyka CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[varshneyhars](https://clawhub.ai/user/varshneyhars)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to have an agent prepare and run Zyka CLI commands for generating or editing video, image, speech, captions, dubbing, and related media outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a mutable globally installed npm CLI.

Mitigation: Install only after reviewing the current `zyka` package and use a trusted, controlled environment for execution.

Risk: Commands can upload local image, audio, and video files to Zyka and downstream providers.

Mitigation: Review exact file paths before execution and avoid private, proprietary, face, or voice media unless rights and consent are clear.

Risk: Agent-driven commands can spend Zyka credits without an additional prompt.

Mitigation: Use restricted API keys with spending limits and review the selected model, estimated cost, and output path before running commands.

## Reference(s):

- [Zyka AI skill page](https://clawhub.ai/varshneyhars/skills/zyka-ai)
- [Zyka website](https://zyka.ai)
- [Zyka CLI npm package](https://www.npmjs.com/package/zyka)
- [Zyka API keys](https://zyka.ai/settings/api-keys)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, text, files]

**Output Format:** [Markdown guidance with inline bash command blocks and CLI output file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the zyka binary and ZYKA_API_KEY; commands may upload referenced local media and save generated outputs to disk.]

## Skill Version(s):

0.4.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
