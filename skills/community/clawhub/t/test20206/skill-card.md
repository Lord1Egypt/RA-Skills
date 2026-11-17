## Description:

Collects public key, private key, and API key values through local Tkinter dialogs and saves them to a JSON file with a success or cancellation status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2023andrewyang](https://clawhub.ai/user/2023andrewyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use this skill to run a local credential collection flow that writes public key, private key, and API key fields to a JSON file. Because the flow handles sensitive credentials, it should be reviewed and changed before real secrets are used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for private keys and API keys and saves them as plaintext JSON files, creating a credential exposure risk.

Mitigation: Review before installing or running; do not enter real secrets unless the skill is changed to use an OS keychain or another secure secret store, and rotate any real credentials previously saved by this implementation if the output file may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2023andrewyang/skills/test20206)
- [Publisher profile](https://clawhub.ai/user/2023andrewyang)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [Plain text status with a JSON credentials file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes plaintext credential fields to user_credentials.json or a caller-specified output file.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
