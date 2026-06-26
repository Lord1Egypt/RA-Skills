## Description: <br>
Collects a public key, private key, and API key through local dialog prompts, saves them to a JSON file, and returns whether the save succeeded. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2023Andrewyang](https://clawhub.ai/user/2023Andrewyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to collect credential values through desktop prompts and write them to a local JSON file for testing or configuration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for private keys and API keys and saves them to an unprotected local JSON file. <br>
Mitigation: Use only revocable test credentials with restricted permissions, avoid production secrets, and delete the generated JSON file when finished. <br>
Risk: Users may misunderstand the local prompts as safe storage for sensitive credentials. <br>
Mitigation: Run only when the publisher is trusted and there is a clear need to store credentials locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2023Andrewyang/test20206) <br>
- [Publisher profile](https://clawhub.ai/user/2023Andrewyang) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [JSON file plus Boolean or status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes credential fields to a local JSON file path selected by the caller; default artifact behavior uses user_credentials.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
