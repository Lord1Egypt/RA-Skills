## Description:

AI music generation assistant powered by MakebestMusic for creating AI-generated music, songs, and audio tracks from user prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sthk-mbm](https://clawhub.ai/user/sthk-mbm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to request custom songs, instrumental tracks, or other generated audio from MakebestMusic and check generation status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill transmits user prompts and an API key to a third-party music-generation service.

Mitigation: Use a dedicated MakeBestMusic key with limited exposure and avoid submitting private or confidential text in prompts.

Risk: The endpoint can be overridden with MBM_API_BASE, which could redirect prompts and credentials to an untrusted service.

Mitigation: Run the skill only in environments where MBM_API_BASE is unset or controlled by a trusted administrator.

## Reference(s):

- [ClawHub Text to Song Skill Page](https://clawhub.ai/sthk-mbm/skills/text-to-song)
- [MakeBestMusic](https://makebestmusic.com/?pid=PIDcLjhgCXUQ)
- [MakeBestMusic API Base](https://api.makebestmusic.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an apiKey environment value and returns music identifiers, task status, and shared music URLs when available.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog mention 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
