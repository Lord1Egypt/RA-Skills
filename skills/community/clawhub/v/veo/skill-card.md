## Description:

Generate video using Google Veo (Veo 3.1 / Veo 3.0).

This skill is ready for commercial/non-commercial use.

## Publisher:

[buddyh](https://clawhub.ai/user/buddyh)

### License/Terms of Use:


## Use Case:

Developers and content creators use this skill to ask an agent to generate MP4 videos from text prompts, with optional reference images, using Google's Veo API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video prompts and selected reference images are sent to Google through the Gemini/Veo API.

Mitigation: Use only prompts and reference images approved for external API processing, and protect the Gemini API key as a secret.

Risk: The Google GenAI dependency is declared with a broad lower-bound version.

Mitigation: Pin or lock the google-genai dependency before running the skill in sensitive or tightly controlled environments.

Risk: The script writes generated MP4 files to user-provided output paths.

Mitigation: Choose output paths in intended working directories and review generated media before sharing or attaching it.

## Reference(s):

- [ClawHub Veo skill page](https://clawhub.ai/buddyh/skills/veo)
- [Buddyh ClawHub publisher profile](https://clawhub.ai/user/buddyh)

## Skill Output:

**Output Type(s):** [shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and MP4 output file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and GEMINI_API_KEY; writes MP4 files and prints a MEDIA line on supported chat providers.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
