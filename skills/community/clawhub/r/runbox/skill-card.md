## Description: <br>
RunBox lets agents execute code in remote, isolated Docker sandboxes through an x402 payment flow using USDC on Stellar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daraijaola](https://clawhub.ai/user/daraijaola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use RunBox when an agent needs to execute, test, benchmark, or inspect code in a remote sandbox across languages such as Python, JavaScript, Bash, Go, Rust, Java, C, C++, TypeScript, and R. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent direct real-money spending authority through a Stellar wallet. <br>
Mitigation: Use a dedicated low-balance wallet, prefer testnet for evaluation, and require confirmation before paid runs. <br>
Risk: Code and inputs are sent to a remote execution service. <br>
Mitigation: Use a trusted HTTPS or self-hosted endpoint and avoid submitting private code, credentials, or sensitive data. <br>


## Reference(s): <br>
- [ClawHub RunBox release page](https://clawhub.ai/daraijaola/runbox) <br>
- [Publisher profile](https://clawhub.ai/user/daraijaola) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON execution results with stdout, stderr, exit code, timing, and optional session metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Stellar wallet secret and may spend USDC when creating paid execution sessions.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
