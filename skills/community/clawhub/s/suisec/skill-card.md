## Description: <br>
Sui Sec pre-simulates Sui client transactions with dry-run output and compares the results with user intent before allowing execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k66inthesky](https://clawhub.ai/user/k66inthesky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Sui users use this skill to gate Sui CLI transaction signing by dry-running PTB or call commands and comparing simulation results with the declared transaction intent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can report SAFE TO SIGN after incomplete transaction checks. <br>
Mitigation: Treat it as a helper only and manually verify the active Sui wallet, exact command, recipients, asset amounts, object changes, call target, gas, and dry-run output before signing. <br>
Risk: The workflow may proceed from dry-run review to real Sui transaction execution. <br>
Mitigation: Block on dry-run failures or mismatches, and require explicit human review before any override. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/k66inthesky/suisec) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and tabular audit output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run Sui CLI dry-run commands and a Python audit helper; requires sui and python3.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact/package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
