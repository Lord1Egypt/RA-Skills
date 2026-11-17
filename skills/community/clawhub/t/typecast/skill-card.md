## Description:

Cast helps agents use the Typecast CLI for multilingual text-to-speech with emotion control, either playing audio aloud or saving it to a file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaebong-human](https://clawhub.ai/user/jaebong-human)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can ask an agent to prepare Typecast CLI commands for synthesizing speech, selecting voices, setting emotion controls, and managing Typecast authentication and configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input text may be sent to Typecast's cloud text-to-speech service.

Mitigation: Do not synthesize secrets, credentials, regulated data, or private text unless Typecast's data handling is acceptable to you.

Risk: Typecast credentials may be stored locally when a user logs in.

Mitigation: Use cast logout or remove ~/.typecast/config.yaml when credentials should no longer be retained.

## Reference(s):

- [ClawHub Cast skill page](https://clawhub.ai/jaebong-human/skills/typecast)
- [ClawHub publisher profile](https://clawhub.ai/user/jaebong-human)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the cast CLI and TYPECAST_API_KEY; may play audio or save wav/mp3 files through the Typecast CLI.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
