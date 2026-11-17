## Description:

Helps agents translate and dub local MP4 videos with SoulDub and retrieve translated videos and subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiabaogithub](https://clawhub.ai/user/jiabaogithub)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and localization teams use the skill to translate local MP4 videos, monitor dubbing jobs, and obtain translated videos and subtitle files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated authentication configuration may direct API-key-bearing requests to a placeholder domain instead of SoulDub.

Mitigation: Verify that api_base points to the real SoulDub API endpoint before entering an API key or running the skill.

Risk: Translation uploads the selected MP4 to SoulDub and creates local output and job-state files.

Mitigation: Use only videos approved for upload and review the resulting local files and active background jobs.

## Reference(s):

- [Source skill (server-resolved provenance)](https://github.com/jiabaogithub/souldub-skills/tree/master/skills/souldub-video-translate)
- [ClawHub skill release](https://clawhub.ai/jiabaogithub/skills/souldub-video-translate)
- [SoulDub Agent API reference](artifact/references/agent-api.md)
- [Supported languages](artifact/references/languages.json)
- [SoulDub API key settings](https://www.souldub.ai/en/settings/apikeys)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with commands, progress summaries, and local result paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports paths to translated MP4 and SRT files or actionable errors.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
