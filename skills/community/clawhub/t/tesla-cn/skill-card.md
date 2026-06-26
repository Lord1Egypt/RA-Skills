## Description: <br>
Remote-control skill for Tesla owners in China that uses Tesla Fleet API access to list vehicles, query vehicle status, and run supported vehicle commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mywind2020](https://clawhub.ai/user/mywind2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Tesla owners and their agents use this skill to configure API access, inspect vehicle information, and issue remote vehicle commands such as wake, lock, climate, trunk, horn, charging-port, and light controls. It is intended for users who can verify vehicle identity and safety conditions before execution. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can issue commands that affect a physical Tesla vehicle. <br>
Mitigation: Require explicit user approval before state-changing commands, start with read-only list or status checks, and confirm the vehicle and surrounding conditions before execution. <br>
Risk: The Tesla API key grants vehicle-control access and is stored locally for command execution. <br>
Mitigation: Treat ~/.tesla_cn.json as a secret file, restrict local access, avoid shared or backed-up systems, and rotate the key if it may have been exposed. <br>
Risk: The security evidence reports a suspicious verdict because commands use tesla.dhuar.com for vehicle-control access. <br>
Mitigation: Install only if the user trusts both the local machine and tesla.dhuar.com with Tesla vehicle-control access. <br>


## Reference(s): <br>
- [Tesla China ClawHub listing](https://clawhub.ai/mywind2020/tesla-cn) <br>
- [Tesla API key service](https://tesla.dhuar.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Markdown guidance with bash commands; command execution returns JSON or plain text responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer and an apiKey stored in ~/.tesla_cn.json or provided during configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
