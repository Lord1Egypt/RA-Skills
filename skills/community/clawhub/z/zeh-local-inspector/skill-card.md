## Description:

Inspect local working directory and return a short result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maosangtianshi](https://clawhub.ai/user/maosangtianshi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to perform a safe, minimal inspection of the current local working directory. It reports the directory path, a short file listing, and concise risk context without modifying files or using the network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reveals the current directory path and a short list of filenames from the directory where it is run.

Mitigation: Use it only in directories the user is comfortable having summarized.

Risk: The skill is documented to return concise Chinese output, which may not match every user's requested language.

Mitigation: Prefer an updated version that respects the user's requested language when language flexibility is required.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Concise Chinese text with local inspection results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only local inspection; reports the current directory path and up to 10 sorted directory entries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
