## Description: <br>
Buddy creates a deterministic gacha-style electronic pet card from a username or supplied name. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subcoldzhang](https://clawhub.ai/user/subcoldzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawHub users use Buddy to run a local Python toy that generates a deterministic electronic pet draw for a username or supplied name. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoking the skill without a name may use the local username or Claw user name as the draw seed. <br>
Mitigation: Pass an explicit non-sensitive name when the generated result should not be tied to a real user name. <br>
Risk: The generic buddy trigger may activate more often than intended. <br>
Mitigation: Use a specific request such as Buddy gacha or electronic pet draw when invoking it intentionally. <br>
Risk: The skill depends on local python3 availability. <br>
Mitigation: Confirm python3 is installed before running the local command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subcoldzhang/test-buddy) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text console output with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deterministic per input name; requires local python3 and does not require network access.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
