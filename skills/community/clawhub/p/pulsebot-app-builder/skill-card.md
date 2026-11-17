## Description:

Build real-time Timeplus data processing and analysis applications in Pulsebot. Creates pure frontend HTML/JavaScript apps that connect directly to Timeplus Proton via @timeplus/proton-javascript-driver (UMD), visualize live streaming data with @timeplus/vistral (UMD), and follow the Timeplus UI style guide. No npm build or bundler required - output is a single self-contained HTML file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gangtao](https://clawhub.ai/user/gangtao)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and data engineers use this skill to create Pulsebot frontend apps for Timeplus Proton streams, including real-time dashboards, pipeline visualizers, streaming analytics views, and data exploration tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated apps may query localhost:8001 as soon as the HTML file opens.

Mitigation: Require a visible manual Connect or Run action that shows the SQL before execution, especially when Proton data is sensitive.

Risk: Generated apps may run mutable JavaScript loaded from unpkg without integrity checks.

Mitigation: Prefer pinned dependency versions with Subresource Integrity or vendored assets before production use.

## Reference(s):

- [Pulsebot App Builder on ClawHub](https://clawhub.ai/gangtao/skills/pulsebot-app-builder)
- [Publisher profile: gangtao](https://clawhub.ai/user/gangtao)
- [Proton JavaScript Driver Reference](references/PROTON_DRIVER.md)
- [Vistral API Reference](references/VISTRAL_API.md)
- [Timeplus Application Style Guide](references/STYLE_GUIDE.md)
- [Timeplus Proton JavaScript Driver](https://github.com/timeplus-io/proton-javascript-driver)
- [Timeplus Vistral](https://github.com/timeplus-io/vistral)
- [Timeplus App Style Guide Source](https://gist.github.com/gangtao/5307e8bbb84384804c7fb9480a515925)

## Skill Output:

**Output Type(s):** [code, files, shell commands, configuration, guidance]

**Output Format:** [Single-file HTML with embedded JavaScript and CSS, plus concise setup or usage notes when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated apps may query the local Proton proxy and load browser dependencies from CDN URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
