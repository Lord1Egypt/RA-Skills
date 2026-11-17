## Description:

Convert text to speech using Hume AI (or OpenAI) API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amstko](https://clawhub.ai/user/amstko)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate MP3 speech audio from text through Hume AI or OpenAI text-to-speech services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Speech text is sent to Hume AI or OpenAI using API keys from the environment.

Mitigation: Use the skill only when sharing the requested text with those services is acceptable, and scope API keys to the intended service account.

Risk: Shell-based invocation with user-controlled text can create command execution risk if arguments are interpolated into a shell command.

Mitigation: Invoke scripts with argument-array execution, or otherwise safely escape user-provided text before execution.

Risk: User-controlled output paths can overwrite arbitrary files.

Mitigation: Write generated audio only to a dedicated media directory and validate output filenames before passing them to the script.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated MP3 file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scripts print a MEDIA line with the absolute path to the MP3 output.]

## Skill Version(s):

1.0.0 (source: server release evidence and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
