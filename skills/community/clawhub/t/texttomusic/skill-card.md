## Description:

AI music generation assistant powered by MakebestMusic for creating AI-generated music, songs, and audio tracks from user prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sthk-mbm](https://clawhub.ai/user/sthk-mbm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to generate vocal or instrumental music from natural-language descriptions and to check the status of generated tracks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a MakeBestMusic API key and sends prompts and generated music IDs to MakeBestMusic.

Mitigation: Use a dedicated key with the minimum needed access, avoid submitting sensitive prompts, and rotate or revoke the key if exposure is suspected.

Risk: The API host can be changed through MBM_API_BASE, which could redirect prompts, music IDs, and the API key if the environment is controlled by untrusted code.

Mitigation: Run the skill only in trusted environments and keep MBM_API_BASE unset or fixed to the official HTTPS endpoint.

Risk: Prompt and music ID arguments are passed through shell-oriented commands in the skill instructions.

Mitigation: Prefer structured argument invocation and review generated commands before execution, especially when prompts include quotes or shell metacharacters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sthk-mbm/skills/texttomusic)
- [MakeBestMusic](https://makebestmusic.com/?pid=PIDcLjhgCXUQ)
- [MakeBestMusic API endpoint](https://api.makebestmusic.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON status responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an apiKey credential for MakeBestMusic and returns generation IDs, status values, and shared music URLs when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
