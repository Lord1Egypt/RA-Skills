## Description: <br>
A simple command-line calculator for basic arithmetic, exponentiation, and modulo expressions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrr000212-netizen](https://clawhub.ai/user/zrr000212-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users use this skill to run quick local math calculations through a command-line Python script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The calculator uses Python eval internally for arithmetic expressions, creating risk from unexpected parser behavior or expensive expressions even with input filtering. <br>
Mitigation: Use only trusted, simple arithmetic expressions; prefer a future AST-based arithmetic parser with input length or computation limits before broader deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text] <br>
**Output Format:** [Plain text results with Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Python script with one arithmetic expression argument.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
