## Description: <br>
Mine Bittensor Subnet 50 (Synth) with Ganglion, including price-path simulation, CRPS scoring, volatility estimation, backtesting, and multi-asset forecasting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tensorlink-dev](https://clawhub.ai/user/tensorlink-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Bittensor miners use this skill to understand and operate SN50 mining workflows with Ganglion, including simulation, scoring, volatility estimation, and backtesting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is documentation-only, but its examples may lead users to run Ganglion, curl, and mining workflows against external APIs or live infrastructure. <br>
Mitigation: Review the separate Ganglion binary and project behavior before real mining, especially wallet, chain, and forecast-submission behavior. <br>
Risk: Forecasting, scoring, and competition parameters can become stale relative to current SN50 validator rules. <br>
Mitigation: Confirm current subnet, validator, and Pyth data-source requirements before relying on the guidance for live submissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tensorlink-dev/skill-8) <br>
- [Ganglion repository](https://github.com/TensorLink-AI/ganglion) <br>
- [Synth subnet reference](https://github.com/mode-network/synth-subnet/tree/main/synth) <br>
- [Pyth Hermes latest price API](https://hermes.pyth.network/v2/updates/price/latest) <br>
- [Pyth Benchmarks history API](https://benchmarks.pyth.network/v1/shims/tradingview/history) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell and API command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; command examples require user review before execution.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
