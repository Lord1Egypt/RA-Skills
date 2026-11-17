## Description:

Web Module Runner is a command-line utility for logging, reviewing, searching, summarizing, and exporting web module task activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to operate a local shell utility that records web module runs, checks, conversions, analyses, comparisons, reports, and exports for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact records arbitrary user input in local history files that can later be searched or exported.

Mitigation: Do not enter secrets, tokens, private paths, or sensitive project details; review local logs and exports before sharing them.

Risk: The package is presented as a web development runner, while server security evidence says the artifacts mainly define a local activity logger.

Mitigation: Review the shell script behavior before installation and use it as a logbook utility unless independent review confirms broader runner behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/skills/web-module-runner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local log and export files under ~/.local/share/web-module-runner/ when the shell script is installed and run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
