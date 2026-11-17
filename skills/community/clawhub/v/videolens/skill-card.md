## Description:

VideoLens turns user-selected YouTube videos, local files, or supported video URLs into timestamped HTML, Markdown, and JSON reports using a pinned local runtime and OpenAI BYOK analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shadoprizm](https://clawhub.ai/user/shadoprizm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, product teams, researchers, and operations users can use this skill to turn videos they are authorized to access into timestamped written reports for summaries, tutorials, meetings, bug review, UX review, privacy review, and creator QA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs an external VideoLens runtime without sandbox or signature verification.

Mitigation: Install only after reviewing that risk and use the pinned runtime and locked dependency flow described by the skill.

Risk: Selected video-derived content and prompts may be sent to OpenAI with the user's API key during analysis.

Mitigation: Use a dedicated low-budget OpenAI key and avoid sensitive videos unless that transmission is acceptable.

Risk: Generated media artifacts and reports may remain in the managed VideoLens state directory.

Mitigation: Remove the managed VideoLens state directory when cached media artifacts and reports should no longer be retained locally.

## Reference(s):

- [VideoLens homepage](https://videolens.io)
- [ClawHub skill listing](https://clawhub.ai/shadoprizm/skills/videolens)
- [shadoprizm publisher profile](https://clawhub.ai/user/shadoprizm)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [JSON status responses with local HTML, Markdown, and JSON report artifact paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis requires explicit credit-spend approval and supports bounded frame and capture settings.]

## Skill Version(s):

1.1.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
