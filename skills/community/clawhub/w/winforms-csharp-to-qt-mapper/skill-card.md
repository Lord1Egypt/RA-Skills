## Description:

Provides C# WinForms to Qt C++ migration guidance and helper scripts for architecture analysis, control mapping, event conversion, layout migration, performance optimization, and testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsgt945](https://clawhub.ai/user/rsgt945)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and execute WinForms-to-Qt migrations, including architecture review, UI/control mapping, event conversion, generated Qt/C++ scaffolding, and migration validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated output can be unsafe when mapping data is unvalidated.

Mitigation: Run the skill on disposable project copies, review mapping JSON before generation, choose an empty output directory, and inspect generated CMake, C++, and UI files before building or running them.

Risk: Analysis reports may overstate incomplete or simulated results.

Mitigation: Treat reports as advisory migration inputs and verify them against the source WinForms project and manual UI, test, and performance checks.

Risk: The artifact is a migration aid rather than a finished automatic converter.

Mitigation: Plan for human review of business logic, complex interactions, UI parity, and performance changes before release.

## Reference(s):

- [WinForms Architecture Analysis Guide](references/architecture_analysis.md)
- [Control Mapping Reference](references/control_mapping.md)
- [Event Conversion Guide](references/event_conversion.md)
- [Layout Migration Guide](references/layout_migration.md)
- [MainControlWrapper Interface Layer Guide](references/interface_layer.md)
- [Qt Performance Optimization Guide](references/performance_optimization.md)
- [Qt Testing Strategy Guide](references/testing_strategy.md)
- [UI Inventory and Specification Checklist](references/ui_inventory_checklist.md)
- [WinForms and Qt UI Differences](references/ui_differences.md)
- [Collapsible UI Components Guide](references/collapsible_ui.md)
- [Qt Documentation](https://doc.qt.io/)
- [Qt Widget Classes](https://doc.qt.io/qt-5/widget-classes.html)
- [Qt Signals and Slots](https://doc.qt.io/qt-5/signalsandslots.html)
- [Qt Layout Management](https://doc.qt.io/qt-5/layout.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON analysis reports, and generated Qt/C++ project files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code and analysis reports require review before build or execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
