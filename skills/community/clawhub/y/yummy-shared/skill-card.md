## Description:

Guides agents through first-time yummycli use, Gemini credential checks, JSON output handling, and shared safety rules for image or video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yummysource](https://clawhub.ai/user/yummysource)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when configuring yummycli with Gemini, validating authentication, interpreting command JSON output, and applying shared CLI safety rules before generation or editing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Gemini API key could be exposed if entered directly into commands that are captured in shell history or agent logs.

Mitigation: Use provider-side key restrictions, avoid typing real keys into logged commands, and rotate any key that may have been exposed.

Risk: The skill depends on the external @yummysource/yummycli package and the yummycli binary.

Mitigation: Install only if the package source is trusted, and prefer a pinned or reviewed package version when possible.

Risk: Generation commands may overwrite a user-specified output path if invoked that way.

Mitigation: Do not overwrite user-specified output paths unless the user intentionally requests that behavior.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown with bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yummycli and GEMINI_API_KEY for Gemini-backed commands.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
