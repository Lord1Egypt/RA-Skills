## Description:

Provides guidance for using PyOmniTS for time series analysis, including documentation links, naming conventions, code patterns, pitfalls, and replication workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ladbaby](https://clawhub.ai/user/ladbaby)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and agents use this skill to navigate PyOmniTS documentation and adapt time series models, datasets, or loss functions into a PyOmniTS installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead agents to clone external research repositories and copy or rewrite code into a local PyOmniTS installation.

Mitigation: Use a trusted repository, pin a reviewed commit, inspect copied files and dependencies, work in a branch or disposable environment, back up the installation, and confirm every file write before applying changes.

Risk: Adapted models, datasets, or loss functions may not match PyOmniTS interfaces or the intended contribution from the source repository.

Mitigation: Review adaptor code against the PyOmniTS API documentation and validate behavior with local tests or experiments before relying on results.

## Reference(s):

- [PyOmniTS GitHub Repository](https://github.com/Ladbaby/PyOmniTS)
- [PyOmniTS Beginner's Guide](https://github.com/Ladbaby/PyOmniTS-docs/blob/main/docs/tutorial/1_get_started.md)
- [PyOmniTS API Reference](https://github.com/Ladbaby/PyOmniTS-docs/blob/main/docs/forecasting/1_API.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with links, numbered steps, and inline code paths or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may involve local file changes in a PyOmniTS installation and should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
