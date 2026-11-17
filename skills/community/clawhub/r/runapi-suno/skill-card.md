## Description:

Generate and transform music, compose or blend lyrics, prepare voice validation phrases, and create reusable custom voices with Suno through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to drive Suno music, audio transformation, lyric, and custom voice workflows through RunAPI while checking current operation contracts before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RunAPI credentials and local media paths may expose sensitive account or content data if included in requests unintentionally.

Mitigation: Review request.json before execution, prefer RUNAPI_API_KEY or saved CLI authentication, and use browser login only when explicitly requested.

Risk: Submitted Suno generation jobs may consume paid API credits or upload media to RunAPI/Suno.

Mitigation: Submit each request once, retry only when evidence shows no task or billing was created, and require user authorization before replacing failed paid tasks.

## Reference(s):

- [RunAPI Suno model homepage](https://runapi.ai/models/suno)
- [Suno model documentation](https://runapi.ai/models/suno.md)
- [Suno provider overview](https://runapi.ai/providers/suno.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI Suno SDK](https://github.com/runapi-ai/suno-sdk)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with JSON request files, shell command blocks, and downloaded media file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include non-media result files in JSON, text, SRT, or VTT plus verified audio downloads when the selected RunAPI operation returns media.]

## Skill Version(s):

0.4.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
