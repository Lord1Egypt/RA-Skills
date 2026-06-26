## Description: <br>
Create local hex and ASCII dumps of binary files for binary analysis, reverse engineering, and protocol debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect binary files as hex and printable ASCII when analyzing firmware, file formats, protocol payloads, or other byte-oriented data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation advertises reverse conversion, patching, JSON, and bit-dump modes that the bundled script does not implement. <br>
Mitigation: Verify the command and supported options before relying on advanced behavior; treat the release as a simple local hex viewer unless separately confirmed. <br>
Risk: Binary patching workflows can corrupt important files if performed directly on originals. <br>
Mitigation: Patch only copies of important binaries and keep a known-good backup for comparison or rollback. <br>


## Reference(s): <br>
- [Xxd Tool on ClawHub](https://clawhub.ai/dinghaibin/xxd-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text hex dump output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file input; the bundled script reads bytes from a file path or standard input and prints offset, hex, and ASCII columns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
