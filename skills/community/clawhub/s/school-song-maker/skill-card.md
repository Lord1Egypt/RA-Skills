## Description:

Turn your school, class, motto, and memories into original lyrics and a sing-along class song, graduation song, or welcome song.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers, class leaders, student groups, and school offices use it to turn school-specific details into singable lyrics and an original song or optional event instrumental.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports broad account permissions and recurring installation tracking beyond school-song creation.

Mitigation: Review the permissions and tracking, and wait to install until their purpose and scope are explained and limited.

Risk: Song material sent to the external music service could contain identifying student details.

Mitigation: Remove identifying student details from material sent to the service.

Risk: The Beatra credential is shared across installed Beatra skills, so removing this package can affect other skills if the shared connection is removed too.

Mitigation: Keep the credential private and use the bundled uninstall flow to check whether other Beatra skills still need the connection.

Risk: An update command changes the installed skill version.

Mitigation: Review the store or tool update command before running it.

Risk: The security assessment is partial: it did not analyze the binary icon and could not resolve some references.

Mitigation: Review the unresolved references and remaining assets before installing.

## Reference(s):

- [School song workflow](artifact/references/workflow.md)
- [Music editing and audio](artifact/references/music-editing-and-audio.md)
- [Tasks and results](artifact/references/tasks-and-results.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [Updates and security](artifact/references/updates-and-security.md)
- [Beatra School Song Maker](https://beatra.ai/skills/school-song-maker)
- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/school-song-maker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Audio, Timed subtitle files, Images]

**Output Format:** [Markdown lyric sheet and generated audio; optional LRC/SRT timing files and cover art]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lyrics-only and one-song modes are available; instrumental, backing, per-class, and extra-file outputs are optional.]

## Skill Version(s):

0.1.9 (source: server-resolved release evidence and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
