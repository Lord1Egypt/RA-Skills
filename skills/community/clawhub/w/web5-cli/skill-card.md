## Description: <br>
Web5 CLI helps agents work with decentralized identity, CKB wallet operations, DID management, PDS data operations, account creation, posting, and profile updates. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[rink1969](https://clawhub.ai/user/rink1969) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate Web5 CLI workflows for DID, CKB wallet, and PDS account tasks, including account creation, deletion, profile updates, and posting. Use it only for proof-of-concept or test-account workflows because the evidence flags high-impact account and credential authority. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may perform destructive account, DID, wallet, or PDS write actions without sufficient safeguards. <br>
Mitigation: Review commands before execution, require explicit confirmation for destructive workflows, and use disposable or test Web5 accounts. <br>
Risk: Credentials, private keys, and JWTs may be exposed or stored unsafely. <br>
Mitigation: Do not use production credentials; redact token output and avoid sharing plaintext key material. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rink1969/web5-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples, command snippets, and Python workflow scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Web5 CLI commands and helper-script guidance for account, DID, wallet, and PDS operations.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
