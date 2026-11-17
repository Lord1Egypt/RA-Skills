## Description:

PythonGO answers questions about PythonGO implementation, APIs, callbacks, errors, modules, installation, debugging, and strategy examples using the bundled codebase and documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aruelius](https://clawhub.ai/user/aruelius)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to answer PythonGO implementation, interface, installation, debugging, and trading strategy questions. It helps generate grounded explanations and complete PythonGO examples from local source, type-reference, and documentation evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated strategy examples can include order placement or cancellation logic that may cause real financial action if run unchanged.

Mitigation: Review generated code first, test in simulation, and do not run order-related examples against live accounts until the behavior is verified.

Risk: Incorrect exchange or contract fields can lead to misleading trading guidance or unintended strategy behavior.

Mitigation: Verify exchange and contract values against the InfiniTrader real-time market or option quote fields before using generated examples.

Risk: Backtesting workflows may process remote files or downloaded archives.

Mitigation: Use trusted data sources, check file integrity before import, and avoid untrusted archive inputs unless the ZIP extraction issue identified in security evidence is fixed.

Risk: Backtesting setup can involve access keys or account credentials.

Mitigation: Keep credentials out of prompts, examples, logs, and shared code; use simulation credentials when testing.

## Reference(s):

- [PythonGO Online Documentation](https://infinitrader.quantdo.com.cn/pythongo_v2)
- [core-pyi.md](references/core-pyi.md)
- [ext-pyi.md](references/ext-pyi.md)
- [PythonGO Documentation Index](docs_normalized/index.md)
- [PythonGO Quick Start](docs_normalized/tutorial/quick_start.md)
- [QuantFair](https://quantfair.quantdo.com.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with Python code blocks and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers are grounded in bundled PythonGO code, type references, indexed documentation, normalized documentation, and examples.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
