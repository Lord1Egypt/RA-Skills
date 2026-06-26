## Description: <br>
Set up and run automated tests for vvvv gamma packages and C# nodes using VL.TestFramework, NUnit, .vl patch assertions, and lightweight agent-driven workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tebjan](https://clawhub.ai/user/tebjan) <br>

### License/Terms of Use: <br>
CC-BY-SA-4.0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, run, and integrate automated tests for vvvv gamma packages, C# nodes, and .vl patches in local or CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated test code or package search paths may load unintended project code during local test execution. <br>
Mitigation: Review generated test code and search paths before running tests, and use the workflow only with trusted repositories. <br>
Risk: Wildcard dependency versions in test project examples can reduce CI reproducibility. <br>
Mitigation: Pin dependency versions in production CI when reproducible test environments are required. <br>


## Reference(s): <br>
- [VL.TestFramework API Reference](artifact/test-framework-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with XML, C#, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and testing guidance for agents; it does not execute tests itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
