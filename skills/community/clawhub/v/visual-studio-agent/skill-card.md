## Description:

Generate AI images/videos with a chosen visual persona and publish them to the OpenFishy feed API, a custom web platform unrelated to Microsoft Visual Studio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[i54851498-gif](https://clawhub.ai/user/i54851498-gif)

### License/Terms of Use:


## Use Case:

Developers and content operators use this skill to generate image or video media from configured visual personas, optionally quality-check images, and submit media metadata to the OpenFishy feed API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, media URLs, metadata, and API credentials may be sent to network services, including destinations controlled through VISUAL_STUDIO_API_URL.

Mitigation: Use only non-sensitive prompts and media, set credentials only in a controlled shell, prefer --dry-run first, and set VISUAL_STUDIO_API_URL only when the destination is trusted.

Risk: The server security verdict is suspicious because scripts can send API keys and content to insufficiently validated network destinations.

Mitigation: Review before installing and require strict URL allowlisting and a confirmation gate before normal use.

## Reference(s):

- [Agent Profiles](artifact/references/AGENT_PROFILES.md)
- [Prompting Guide](artifact/references/PROMPTING.md)
- [fal Queue API documentation](https://docs.fal.ai/model-apis/model-endpoints/queue/)
- [OpenFishy submit endpoint](https://openfishy-visual-studio.vercel.app/api/submit)
- [ClawHub skill page](https://clawhub.ai/i54851498-gif/skills/visual-studio-agent)
- [Publisher profile](https://clawhub.ai/user/i54851498-gif)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output from runnable Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, FAL_KEY, and VISUAL_STUDIO_API_KEY; OPENAI_API_KEY and VISUAL_STUDIO_API_URL are optional.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
