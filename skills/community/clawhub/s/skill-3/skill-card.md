## Description:

Skill 3 is a zero-dependency JSON utility that pretty-prints, validates, minifies, sorts keys, and queries JSON with dot-notation paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claudiodrusus](https://clawhub.ai/user/claudiodrusus)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to format, validate, minify, sort, and query JSON files or stdin data during local development and shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive JSON can be exposed or mishandled when data is piped from an untrusted source.

Mitigation: Use stdin and curl-style pipelines only with trusted sources, and avoid processing confidential JSON from untrusted locations.

Risk: The output option writes to a user-selected file path.

Mitigation: Review the output path before running commands that use -o or --output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claudiodrusus/skills/skill-3)
- [ClawHub publisher profile](https://clawhub.ai/user/claudiodrusus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON or plain-text command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled Python utility can read from a JSON file or stdin and can write formatted, minified, sorted, queried, or validation output to stdout or a selected output file.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
