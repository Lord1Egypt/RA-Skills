## Description:

Generates instrumental music, vocal songs, or lyrics with Tianpuyue AI, polls task status, and saves generated results locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[showtimewalker](https://clawhub.ai/user/showtimewalker)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, multimedia workflow operators, and developers use this skill to create background music, full songs with vocals, or lyrics through Tianpuyue and retrieve the local results for later delivery or integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Output filenames can escape the promised output folder when unsafe names are supplied.

Mitigation: Use a dedicated, low-risk OUTPUT_ROOT and pass only simple short filenames until filename validation and containment checks are enforced.

Risk: Prompts, optional lyrics, task IDs, and the API key are sent to Tianpuyue, and generated files and logs persist locally.

Mitigation: Avoid sending sensitive prompts or lyrics, protect TIANPUYUE_API_KEY, and review or clean the local output and log directories after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/showtimewalker/skills/tianpuyue-music)
- [Voice ID map](references/voice_id_map.md)
- [Tianpuyue voice selection page](https://www.tempolor.com/create/song)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Shell commands that return JSON summaries and save local audio or Markdown lyric files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TIANPUYUE_API_KEY and uv; OUTPUT_ROOT can direct where generated files and logs are written.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
