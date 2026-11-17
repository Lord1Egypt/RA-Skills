## Description:

Video Editing Agent (VEA) helps agents index videos, create highlight reels, generate narration and subtitles, select background music, and produce edited video outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnshenopeninterx](https://clawhub.ai/user/shawnshenopeninterx)

### License/Terms of Use:


## Use Case:

Developers, video creators, and agent operators use this skill to run a local VEA service, index source videos, and produce edited outputs such as highlight reels, shorts, narrated videos, subtitles, and background-music mixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation flow and helper scripts run local shell commands, install dependencies, and start a local server.

Mitigation: Review the scripts before use and prefer a safer uv installation method in a controlled environment.

Risk: Untrusted project names, prompts, ports, or VEA_DIR values may affect helper-script behavior.

Mitigation: Use trusted values only, quote and validate inputs, and avoid running helper scripts against untrusted project directories.

Risk: The VEA config file stores API keys for Memories.ai, Google/Gemini, ElevenLabs, and optionally Soundstripe.

Mitigation: Keep ~/vea/config.json owner-readable only, avoid committing it, and rotate keys if exposure is suspected.

Risk: Video frames, derived text, narration, subtitles, or audio requests may be sent to external services depending on enabled features.

Mitigation: Confirm user consent and data-handling requirements before enabling Memories.ai, Google/Gemini, ElevenLabs, or Soundstripe-backed workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shawnshenopeninterx/skills/vea)
- [VEA GitHub Repository](https://github.com/Memories-ai-labs/vea-open-source)
- [VEA Paper](https://arxiv.org/abs/2509.16811)
- [API Documentation](references/api.md)
- [Config Schema](references/config.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown instructions with bash commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl requests, local file paths, server settings, and video-processing options.]

## Skill Version(s):

1.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
