## Description:

Generate WeryAI music, vocal songs, or instrumental tracks through the WeryAI music API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weryai-developer](https://clawhub.ai/user/weryai-developer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit WeryAI music generation jobs, check balances, poll task status, and deliver generated audio links for vocal-song or instrumental workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is marked suspicious because it ships undisclosed podcast-generation code alongside the music workflow.

Mitigation: Remove the bundled podcast code or disclose and review it before treating the release as a tightly scoped music-only skill.

Risk: API credentials and generated media requests can be exposed to an untrusted endpoint if WERYAI_BASE_URL is changed.

Mitigation: Use the official WeryAI API host unless the replacement endpoint is controlled and trusted.

Risk: Local reference_audio paths may upload local files to the WeryAI service.

Mitigation: Avoid local reference_audio paths unless the user intends to upload that file.

Risk: Paid submit or wait runs can spend WeryAI credits.

Mitigation: Confirm paid generation parameters before running submit or wait, and use dry-run or balance checks when appropriate.

Risk: Arbitrary webhook URLs may send task callbacks to an unintended destination.

Mitigation: Use only webhook URLs that are expected, public, and trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/weryai-developer/skills/weryai-music-generator)
- [Publisher Profile](https://clawhub.ai/user/weryai-developer)
- [Music API Reference](references/api-music.md)
- [Error Codes](references/error-codes.md)
- [WeryAI API Keys](https://www.weryai.com/api/keys)
- [WeryAI API Host](https://api.weryai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON command output and audio links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include task status, audio URLs, lyrics, cover URL, balance, request summaries, and structured error details.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
