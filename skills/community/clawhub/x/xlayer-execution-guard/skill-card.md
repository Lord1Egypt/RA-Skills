## Description: <br>
Runs an executable X Layer pre-execution guard for autonomous agents, combining OnchainOS DEX route judgment, honeypot and price-impact checks, proof-mode evidence, and optional Agentic Wallet execution via onchainos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard7463](https://clawhub.ai/user/richard7463) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent operators use this skill to evaluate X Layer swap intents, block or resize risky routes, generate proof-mode evidence, and optionally execute approved wallet swaps with post-execution proof artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live agentic-wallet mode can trigger real wallet swaps. <br>
Mitigation: Use proof mode or --no-execute by default, require explicit user approval for live wallet actions, and limit live runs to wallets and amounts the user is prepared to risk. <br>
Risk: Broad local credentials can be passed into subprocess execution or picked up from environment files. <br>
Mitigation: Review .env and .env.local files before use, keep OnchainOS credentials scoped to intended runs, and avoid setting EXECUTION_GUARD_EXECUTION_MODE=agentic-wallet globally. <br>
Risk: Missing OnchainOS API credentials can produce mock output that may be confused with live proof. <br>
Mitigation: Treat mock output as install verification only and require configured API credentials plus a real transaction hash before presenting output as live execution proof. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richard7463/xlayer-execution-guard) <br>
- [OnchainOS API base](https://web3.okx.com) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [JSON guard/proof artifacts and Markdown guidance with bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Proof mode produces simulated execution evidence; live agentic-wallet mode may produce transaction hashes after approved wallet execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and plugin.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
