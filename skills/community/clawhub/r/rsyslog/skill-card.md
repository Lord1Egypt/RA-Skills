## Description:

RSyslog advanced system logging reference. RainerScript configuration, input/output modules (imtcp/imfile/omfwd/omelasticsearch), templates with property replacer, content-based filtering, TLS-encrypted remote logging, queue performance tuning, and debug troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and systems engineers use this skill as a command-driven RSyslog reference for Linux logging configuration, forwarding, filtering, templates, performance tuning, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote logging examples may be copied into production without authenticated TLS peer validation.

Mitigation: Use authenticated TLS with permitted peer names before deploying remote forwarding examples.

Risk: Dynamic file path examples can write logs into broad or unexpected filesystem paths.

Mitigation: Constrain dynamic file paths to approved directories and naming patterns.

Risk: Configuration snippets may fail or behave differently in a target RSyslog environment.

Mitigation: Validate configurations with rsyslogd before applying them.

Risk: Queue and disk settings may be too small, too large, or unsuitable for the deployment.

Mitigation: Set queue and disk limits based on the environment's capacity and retention needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/rsyslog)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reference text with shell and RainerScript configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command-selected reference sections]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
