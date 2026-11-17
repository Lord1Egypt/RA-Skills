## Description:

Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy. (Modified to use Opencode instead of Claude Code CLI - auto-detects opencode location)

This skill is ready for commercial/non-commercial use.

## Publisher:

[pwu0125](https://clawhub.ai/user/pwu0125)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to draft new agent skills, improve existing skills, create evaluation prompts, run Opencode-based evaluation loops, review qualitative and benchmark results, and package finished skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluation and description optimization run external Opencode agent processes that may process skill contents, prompts, outputs, and feedback.

Mitigation: Run these workflows only with trusted skills and workspaces, review prompts before execution, and use Opencode configuration appropriate for the data sensitivity.

Risk: Bundled scripts can write local files, package skill archives, and interact with local review artifacts.

Mitigation: Use a disposable or copied workspace for review, inspect generated files and package contents before sharing, and avoid running the packager on untrusted skill directories.

Risk: The review viewer and generated HTML may expose untrusted skill outputs or feedback in a browser context.

Mitigation: Prefer static review output for untrusted inputs, avoid opening generated viewers with sensitive content, and treat embedded outputs as review material rather than trusted web content.

Risk: Local server workflows and process cleanup can affect occupied ports or unrelated local processes if used carelessly.

Mitigation: Choose unused ports, prefer static HTML in constrained environments, and verify process identifiers before stopping any local server.

## Reference(s):

- [Skill Creator JSON Schemas](references/schemas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON examples, shell commands, generated skill files, evaluation reports, benchmark summaries, static HTML review pages, and packaged skill archives.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.9+ and Opencode CLI for automated evaluation and description optimization workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
