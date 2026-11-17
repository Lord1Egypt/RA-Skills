## Description:

Mine Bittensor Subnet 50 (Synth) with Ganglion, covering price-path simulation, CRPS scoring, volatility estimation, backtesting, and multi-asset forecasting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tensorlink-dev](https://clawhub.ai/user/tensorlink-dev)

### License/Terms of Use:


## Use Case:

Developers and Bittensor miners use this skill to understand and operate Ganglion-based Synth forecasting workflows for Subnet 50. It provides guidance for generating Monte Carlo price paths, using Pyth price data, estimating volatility, and backtesting CRPS performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands may target an unintended Ganglion service if GANGLION_URL is misconfigured.

Mitigation: Set GANGLION_URL only to the intended local or trusted server before running remote workflow examples.

Risk: Python dependency drift can change forecasting or scoring behavior.

Mitigation: Install dependencies in a virtual environment and pin versions when reproducing mining or backtesting workflows.

Risk: Forecast submissions can be rejected when timestamps, increments, path counts, path lengths, or price precision do not match validator requirements.

Mitigation: Validate generated submissions against the documented Synth format before submitting them to validators.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tensorlink-dev/skills/skill-8)
- [Ganglion project](https://github.com/TensorLink-AI/ganglion)
- [Synth subnet reference](https://github.com/mode-network/synth-subnet/tree/main/synth)
- [Pyth Hermes latest price API](https://hermes.pyth.network/v2/updates/price/latest)
- [Pyth Benchmarks history API](https://benchmarks.pyth.network/v1/shims/tradingview/history)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflows require either the ganglion binary or curl; no credential environment variables were detected.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
