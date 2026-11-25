## Description:

Functional skill. Coordinate multi-agent cross-device encrypted collaboration using MGC 1.6.0 chain mode. Split a workflow by data domain into N sealed sub-packages; each execution agent receives only the scripts authorized for it. Data and credentials never leave local storage; only task cards, scripts, and result summaries flow across devices. Default dispatch is email; task payloads travel as sealed sub-packages. Includes role-reference task-card templates, a credential-access example, and a task-flow template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to split cross-device workflows among agents by data domain, deliver recipient-specific sealed script packages, and return concise summaries while keeping each executor's data and credentials local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a medium-confidence suspicious verdict, citing incomplete analysis, a mismatch between the stated collaboration purpose and supplied examples, and an unsafe-handling concern for external summaries.

Mitigation: Review supplied examples and externally returned summary scripts before execution; verify package hashes and granted files, and confirm that reported file and network access fits the intended workflow.

## Reference(s):

- [MGC-Blackbox project](https://github.com/zkeviny/MGC-Blackbox)
- [ClawHub skill release](https://clawhub.ai/zkeviny/skills/sealed-chain-en)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes role prompts, workflow templates, package grant specifications, and result-summary guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
