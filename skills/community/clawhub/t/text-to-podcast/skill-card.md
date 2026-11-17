## Description:

Converts text scripts and articles into podcast-style MP3 audio with configurable TTS voice, model, speed, preview, and batch options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and content teams use this skill to convert Markdown or text scripts into podcast audio for drafts, previews, batch production, and content repurposing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and uninstall scripts can write or delete configuration and output files in the parent directory instead of only the skill directory.

Mitigation: Review the resolved paths before running scripts, avoid elevated privileges, use an isolated virtual environment, and confirm cleanup prompts before deletion.

Risk: Text submitted for conversion is sent to OpenAI's TTS API.

Mitigation: Avoid processing confidential, regulated, or sensitive text unless that external processing is approved for the intended use.

Risk: The install script installs Python dependencies without pinning exact versions.

Mitigation: Prefer a virtual environment with reviewed and pinned dependency versions before commercial use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utopiabenben/skills/text-to-podcast)
- [Publisher profile](https://clawhub.ai/user/utopiabenben)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [MP3 audio files with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENAI_API_KEY; supports single-file conversion, batch conversion, preview mode, voice selection, model selection, speed adjustment, and custom output paths.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
