## Description: <br>
PythonGO helps agents answer questions about PythonGO code, documentation, callbacks, errors, modules, functions, installation, and strategy examples using the bundled codebase and docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aruelius](https://clawhub.ai/user/aruelius) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and PythonGO users use this skill to answer implementation, API, installation, debugging, and strategy-example questions grounded in the bundled PythonGO codebase, indexed documentation, normalized docs, and type references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated strategy or API guidance may affect trading behavior if run without review. <br>
Mitigation: Review generated strategy code before running it and test in simulation or paper mode first. <br>
Risk: Installer and dependency examples reference downloadable executables or packages. <br>
Mitigation: Use trusted PythonGO or InfiniTrader sources, avoid untrusted downloads, and do not bypass security warnings unless the source is verified. <br>
Risk: Credentials or account access may be involved when applying examples. <br>
Mitigation: Do not hardcode real credentials, and keep secrets outside generated code. <br>


## Reference(s): <br>
- [PythonGO online documentation](https://infinitrader.quantdo.com.cn/pythongo_v2) <br>
- [PythonGO local documentation index](docs_normalized/index.md) <br>
- [PythonGO core type reference](references/core-pyi.md) <br>
- [PythonGO extension type reference](references/ext-pyi.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with code blocks and file/path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Grounded in bundled PythonGO code, documentation indexes, normalized docs, and type reference files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
