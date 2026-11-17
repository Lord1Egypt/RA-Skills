## Description:

Generates Word Jumble puzzles with scrambled words, circled clue letters, a final idiom answer, a cartoon hint image, and a printable puzzle screenshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robin-marv](https://clawhub.ai/user/robin-marv)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and agents use this skill to generate daily-style word jumble puzzles, validate their puzzle structure, render printable puzzle images, and return generated files for posting or scheduling elsewhere.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering untrusted puzzle JSON or image filenames may expose users to renderer hardening issues.

Mitigation: Use the skill for puzzles you generate or otherwise trust, and avoid untrusted puzzle JSON or image filenames until HTML escaping and validator checks are fixed.

Risk: Cartoon image prompts are sent to the configured external image generation provider.

Mitigation: Do not include sensitive or confidential information in image generation prompts.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, image files]

**Output Format:** [Markdown response with file paths, JSON puzzle data, generated image files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a puzzle JSON file, a cartoon JPG, and a printable PNG; posting and scheduling are handled by the caller.]

## Skill Version(s):

1.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
