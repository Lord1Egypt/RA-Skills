## Description: <br>
Reads local text-oriented files with GBK-first and UTF-8 fallback encoding detection, including DOCX and text-based PDF extraction when optional dependencies are available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Delicate314](https://clawhub.ai/user/Delicate314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect local files that may use Chinese Windows encodings, and to extract text from DOCX or text-based PDF files when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local files that the agent is pointed at, which may expose sensitive documents or credentials if the selected path is inappropriate. <br>
Mitigation: Use it only on files intended for the task, and avoid credential stores, private configuration files, and personal documents unless their contents should be shared. <br>
Risk: Reading DOCX or PDF files can trigger automatic pip installation of optional Python dependencies. <br>
Mitigation: Preinstall approved dependencies in controlled environments, or avoid DOCX/PDF inputs when automatic package installation is not acceptable. <br>
Risk: Unsupported binary files, scanned PDFs, and very large files may fail, produce little text, or return truncated content. <br>
Mitigation: Use supported text-oriented files and verify the returned content before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Delicate314/read-gbk) <br>
- [Python downloads](https://www.python.org/downloads/) <br>
- [Miniconda documentation](https://docs.conda.io/en/latest/miniconda.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text file contents on stdout with status or error messages on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads an explicitly provided local file path; DOCX/PDF support may install optional Python packages and very large or unsupported files may fail or be truncated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
