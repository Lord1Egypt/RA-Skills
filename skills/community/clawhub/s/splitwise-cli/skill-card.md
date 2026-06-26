## Description: <br>
Manage shared expenses, balances, and settlements through the Splitwise CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barronlroth](https://clawhub.ai/user/barronlroth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who use Splitwise can ask an agent to check balances, list expenses, create shared expenses, record settlements, and delete expense records through an authenticated Splitwise CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated Splitwise commands can change, settle, or delete shared expense records. <br>
Mitigation: Confirm the group, people, payer, amount, currency, split, settlement target, and expense ID before any state-changing command, especially deletion. <br>
Risk: The agent could operate the wrong Splitwise account or an unintended CLI binary. <br>
Mitigation: Verify that the splitwise binary on PATH and the OAuth/config files are the intended ones before using the skill. <br>


## Reference(s): <br>
- [Declared Splitwise CLI homepage](https://github.com/example/splitwise-cli) <br>
- [ClawHub skill page](https://clawhub.ai/barronlroth/splitwise-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may use Splitwise CLI output modes such as JSON, quiet output, or no-color output.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
