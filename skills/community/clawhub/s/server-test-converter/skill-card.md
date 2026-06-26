## Description: <br>
Converts server command text files into pytest test cases, generating one test file per input file and using a configurable test framework for execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyun2025](https://clawhub.ai/user/liuyun2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to convert server or NIC command lists into pytest files for R5-card or host-shell test execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated pytest tests can run real server commands from input .txt files. <br>
Mitigation: Review the input command files and generated test_*.py files before running pytest, and use only trusted command sources. <br>
Risk: Generated tests depend on test_framework.py to execute commands against the intended environment. <br>
Mitigation: Use a trusted test_framework.py implementation, avoid hardcoding real SSH passwords, and confirm target device settings before execution. <br>
Risk: Generated output may replace existing test files in the configured output directory. <br>
Mitigation: Run the converter only in a directory where overwriting generated tests is acceptable. <br>


## Reference(s): <br>
- [Server Test Converter on ClawHub](https://clawhub.ai/liuyun2025/server-test-converter) <br>


## Skill Output: <br>
**Output Type(s):** [code, files, shell commands, configuration, guidance] <br>
**Output Format:** [Python pytest files with Markdown guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates one pytest file per input .txt command file; generated tests depend on a trusted local test_framework.py configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
