## Description: <br>
Creates, configures, and deploys on-chain automation workflows using the Ditto Network SDK for scheduled, event-triggered, or condition-based EVM transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vladislavshad](https://clawhub.ai/user/vladislavshad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, simulate, deploy, monitor, and cancel Ditto Network workflows for EVM automation such as recurring transfers, scheduled swaps, event-triggered contract calls, and on-chain state conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents through workflows that use raw wallet private keys and can automate transactions with real funds. <br>
Mitigation: Use a dedicated low-balance wallet, keep private keys in local environment variables outside version control, and avoid exposing secrets in chat, logs, or shared machines. <br>
Risk: Production EVM automation can execute incorrect, mistimed, or economically unsafe transactions. <br>
Mitigation: Test on Sepolia or Base Sepolia first, review generated workflow code and contract parameters before execution, and require explicit confirmation before production deployment. <br>
Risk: Unpinned or unreviewed SDK dependencies and weak swap parameters can increase execution or loss risk. <br>
Mitigation: Pin and review the Ditto SDK dependency, avoid production swaps with zero slippage protection, and confirm cancellation and monitoring steps before using real funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vladislavshad/workflow-automation-evm-wallets) <br>
- [Ditto Workflow SDK](https://github.com/dittonetwork/ditto-workflow-sdk) <br>
- [Ditto IPFS service](https://ipfs-service.dittonetwork.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include EVM addresses, workflow schedules, environment variable names, contract call parameters, and verification steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
