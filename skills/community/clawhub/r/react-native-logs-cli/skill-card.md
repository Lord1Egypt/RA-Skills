## Description: <br>
Use rn-logs to read React Native Metro logs via CDP, with plain-text output for non-interactive agent runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okwasniewski](https://clawhub.ai/user/okwasniewski) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
React Native developers and agents use this skill to install and run rn-logs, list connected apps, stream Metro logs, and capture bounded log snapshots from a running app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party rn-logs-cli package. <br>
Mitigation: Install and use it only when the package and publisher are trusted. <br>
Risk: React Native logs may contain tokens, user data, or debug details. <br>
Mitigation: Treat captured logs as sensitive and prefer bounded snapshots such as --limit when full streaming is unnecessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/okwasniewski/react-native-logs-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and plain-text log output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can stream logs or capture bounded snapshots with --limit.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; SKILL.md metadata says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
