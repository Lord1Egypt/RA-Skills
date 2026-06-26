## Description: <br>
Tableau helps agents guide conversion of Excel, CSV, XML, and YAML configuration data into Protobuf-backed JSON, Text, or binary outputs through the tableauc protogen and confgen pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenchy](https://clawhub.ai/user/wenchy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when building or validating tableau configuration workbooks and related config files, especially when they need the agent to prepare inputs, run tableauc, and explain generated Protobuf-backed outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to create or modify local conversion files and run tableauc in the workspace. <br>
Mitigation: Use the default temp/ workspace or version control, and review generated file paths before running the workflow on project files. <br>
Risk: Installing or invoking tableauc may introduce toolchain or version risk. <br>
Mitigation: Approve or perform the Go installation yourself and prefer a pinned, trusted tableauc version. <br>


## Reference(s): <br>
- [Official Tableau Documentation Repository](https://github.com/tableauio/tableauio.github.io) <br>
- [Tableau Test Cases Repository](https://github.com/tableauio/tableau) <br>
- [config.yaml / options.Options Reference](references/config.md) <br>
- [Metasheet (@TABLEAU) Reference](references/metasheet.md) <br>
- [Protoconf Annotation Reference](references/protoconf.md) <br>
- [Type System Deep Dive](references/types.md) <br>
- [Excel Input Format Reference](references/excel/index.md) <br>
- [Excel Styling](references/excel/styling.md) <br>
- [CSV Input Format Reference](references/csv/index.md) <br>
- [XML Input Format Reference](references/xml/index.md) <br>
- [YAML Input Format Reference](references/yaml/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local spreadsheet and configuration files, then run tableauc to generate Protobuf-backed config outputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
