## Description:

List, test, and extract files from ZIP archives. Use when you need to decompress or inspect ZIP file contents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to unpack ZIP archives into a selected directory during file handling workflows. Review before use because the security evidence says documented listing, testing, overwrite controls, and selective extraction are not implemented by the bundled extractor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation advertises archive listing, testing, overwrite controls, and selective extraction, but the security evidence says the bundled script does not implement those behaviors.

Mitigation: Use it only in an empty temporary directory, inspect ZIP contents with another trusted tool first, and do not rely on -l, -n, -o, or selective extraction behavior.

Risk: The bundled extractor writes ZIP contents to disk in the target directory.

Mitigation: Run extraction in an empty temporary directory and review the extracted files before moving them into a project or shared location.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Markdown guidance with command-line examples and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May extract files to disk in the requested directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
