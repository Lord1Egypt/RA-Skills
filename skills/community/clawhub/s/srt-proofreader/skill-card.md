## Description:

Proofread SRT subtitles by using srts/source.md as terminology reference while preserving subtitle indices and timestamps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kapiai](https://clawhub.ai/user/kapiai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to proofread subtitle files in srts/*.srt against srts/source.md terminology while preserving SRT indices, timestamps, line structure, and git-tracked change review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initialize a git repository, create a baseline commit, and overwrite the selected SRT file as part of normal proofreading.

Mitigation: Keep unrelated or sensitive files out of srts/ and review git diff before accepting the result.

Risk: Incorrect or incomplete srts/source.md terminology can lead to incorrect subtitle wording.

Mitigation: Review srts/source.md before running the workflow and verify corrected term categories in the final summary.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and edited SRT subtitle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves subtitle indices and timestamps; may split SRT files over 400 lines into section files and merge them back.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
