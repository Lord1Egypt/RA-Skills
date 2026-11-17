## Description:

Shipcheck helps agents run the @symbolstar/shipcheck CLI before publishing an npm package, OpenClaw skill folder, or repository to catch likely PII, infrastructure, business-term, binary, and secret leaks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[symbolstar](https://clawhub.ai/user/symbolstar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill before npm publish, clawhub publish, or making a repository public to scan likely release contents and triage PII or secret findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an unpinned third-party npm scanner over repositories that may contain sensitive source files.

Mitigation: Install only a trusted, reviewed version of @symbolstar/shipcheck, run it on an explicit path, and consider sandboxing or blocking outbound network access when scanning sensitive code.

Risk: The scanner is best-effort and is not a replacement for manual review or a full secret scanner.

Mitigation: Use it as a pre-publish check alongside manual review and dedicated secret scanners, then rerun until critical and high findings are cleared.

## Reference(s):

- [Shipcheck ClawHub Skill](https://clawhub.ai/symbolstar/skills/shipcheck)
- [@symbolstar/shipcheck npm package](https://www.npmjs.com/package/@symbolstar/shipcheck)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and finding triage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of the shipcheck CLI, including scan modes, allow-list configuration, exit-code interpretation, and rerun workflow.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
