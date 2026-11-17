## Description:

Use when the user wants to create, translate, import, validate, inspect, or update powerlifting training programs or workout logs for SigmaLifting using sigmalifting-cli, especially from spreadsheets, manuals, public programs, app exports, program-import bundles, or process-import bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sigmalifting-dev](https://clawhub.ai/user/sigmalifting-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate SigmaLifting CLI workflows for modeling, importing, validating, inspecting, and updating powerlifting program and process bundles. It is especially suited for translating spreadsheets, manuals, public programs, app exports, and workout logs into CLI-validated SigmaLifting artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install path asks users to globally install mutable remote code from GitHub.

Mitigation: Review the CLI source and prefer a pinned commit, signed release, exact package version, or project-local install before using the skill.

Risk: Program and process bundle changes can persist to the default local CLI store.

Mitigation: Use SIGMALIFTING_HOME or --store-root for test and project-local work so training data changes stay in the intended store.

Risk: Direct edits to SigmaLifting JSON can bypass validation or corrupt program and process bundle semantics.

Mitigation: Create, update, validate, and normalize bundles through sigmalifting-cli commands instead of manual file edits.

## Reference(s):

- [SigmaLifting CLI skill page](https://clawhub.ai/sigmalifting-dev/skills/sigmalifting-cli)
- [SigmaLifting CLI repository](https://github.com/sigmalifting/cli.git)
- [Program Modeling](references/program-modeling.md)
- [Process Logging](references/process-logging.md)
- [Candito Translation](references/candito-translation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI-generated JSON bundle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses sigmalifting-cli as the validation and mutation engine; direct JSON mutation is out of scope.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
