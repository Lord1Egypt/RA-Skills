## Description: <br>
Use when the user wants to create, translate, import, validate, inspect, or update powerlifting training programs or workout logs for SigmaLifting using sigmalifting-cli, especially from spreadsheets, manuals, public programs, app exports, program-import bundles, or process-import bundles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sigmalifting-dev](https://clawhub.ai/user/sigmalifting-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate SigmaLifting CLI workflows for modeling, importing, validating, inspecting, and updating powerlifting program and workout-log bundles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Global installation and CLI-backed mutations can affect local SigmaLifting program or workout-log data. <br>
Mitigation: Verify the upstream sigmalifting-cli repository, prefer a pinned trusted version, and use SIGMALIFTING_HOME or --store-root for a test or project-specific store before modifying real data. <br>


## Reference(s): <br>
- [SigmaLifting CLI repository](https://github.com/sigmalifting/cli.git) <br>
- [ClawHub release page](https://clawhub.ai/sigmalifting-dev/sigmalifting-cli) <br>
- [Program Modeling](references/program-modeling.md) <br>
- [Candito Translation](references/candito-translation.md) <br>
- [Process Logging](references/process-logging.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be validated through sigmalifting-cli before import or persistence.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
