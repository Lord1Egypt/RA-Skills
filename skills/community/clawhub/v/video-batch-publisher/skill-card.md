## Description:

A local batch video publishing skill that helps users configure and run a Python/Playwright tool to publish videos from Excel to Douyin, WeChat Channels, Kuaishou, and Bilibili with titles, descriptions, covers, tags, collections, and scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chencong501](https://clawhub.ai/user/chencong501)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, media operators, and developers use this skill to set up and operate a local GUI or command-line workflow for batch publishing short-form videos across supported platforms from an Excel task list. The agent provides setup, configuration, command, and troubleshooting guidance; the user remains responsible for logging in and reviewing publication behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled tool can publish publicly by reusing locally stored browser login sessions.

Mitigation: Use it only on trusted machines and accounts, start with draft mode or a small test batch, and protect or delete browser_cache when finished.

Risk: Browser automation may violate platform terms or trigger account risk controls.

Mitigation: Confirm platform rules before use, avoid high-volume unattended batches, and stop if a platform presents verification or enforcement warnings.

Risk: Logs, screenshots, and output files may contain sensitive account, video, or publishing details.

Mitigation: Review generated logs and screenshots before sharing them, and remove sensitive local artifacts after troubleshooting.

Risk: The security guidance flags unsafe subprocess openers and recommends dependency hardening before operational use.

Mitigation: Pin dependencies and review or fix local file-opening subprocess calls before using the tool in routine workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chencong501/skills/video-batch-publisher)
- [Setup guide](references/setup.md)
- [Capability matrix](references/capability-matrix.md)
- [Evaluation and risk notes](references/evaluation.md)
- [Packaging plan](references/packaging-plan.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides local execution of the bundled publisher; publishing actions occur through the user's local browser session.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
