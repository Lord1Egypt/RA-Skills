## Description: <br>
Provides C# WinForms to Qt C++ migration guidance and helper tooling for architecture analysis, control mapping, event conversion, layout migration, performance optimization, and testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RSGT945](https://clawhub.ai/user/RSGT945) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and execute migrations from C# WinForms applications to Qt C++, including architecture refactoring, UI/control mapping, event conversion, generated code scaffolding, and validation planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated migration analysis may be incomplete or overstated. <br>
Mitigation: Treat results as best-effort guidance and manually review architecture findings, mappings, and generated code before relying on them. <br>
Risk: Helper scripts may write files into user-specified output paths. <br>
Mitigation: Run the skill in a sandbox or against a copy of the repository, and choose a new empty output directory for generated artifacts. <br>
Risk: Dependencies and local code-processing behavior may be unsuitable for sensitive or proprietary repositories without review. <br>
Mitigation: Audit or update dependencies and review the skill limitations before using it with sensitive code. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/RSGT945/winforms-csharp-to-qt-mapper) <br>
- [Architecture analysis guide](references/architecture_analysis.md) <br>
- [Interface layer guide](references/interface_layer.md) <br>
- [Control mapping reference](references/control_mapping.md) <br>
- [Event conversion guide](references/event_conversion.md) <br>
- [Layout migration guide](references/layout_migration.md) <br>
- [Performance optimization guide](references/performance_optimization.md) <br>
- [Testing strategy guide](references/testing_strategy.md) <br>
- [UI inventory checklist](references/ui_inventory_checklist.md) <br>
- [Qt documentation](https://doc.qt.io/) <br>
- [Qt widget classes](https://doc.qt.io/qt-5/widget-classes.html) <br>
- [Qt signals and slots](https://doc.qt.io/qt-5/signalsandslots.html) <br>
- [Qt layout management](https://doc.qt.io/qt-5/layout.html) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated code snippets, and JSON analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write analysis reports and generated Qt/C++ project files when helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
