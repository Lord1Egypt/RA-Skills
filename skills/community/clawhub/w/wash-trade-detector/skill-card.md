## Description: <br>
Detects and flags wash trades in NFT transaction data using 7 confidence-weighted patterns, protecting all downstream scoring and signals from artificial inflation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PaperBuddha](https://clawhub.ai/user/PaperBuddha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to assess NFT sales records for wash-trade indicators and return a structured confidence, status, weighting, and exclusion assessment for downstream scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: NFT transactions may be under- or over-flagged if the calling agent uses thresholds or exclusion handling that do not match its scoring policy. <br>
Mitigation: Confirm confidence thresholds, weight multipliers, and downstream exclusion behavior before installing or relying on the skill. <br>
Risk: The skill analyzes transaction data supplied by the caller and does not independently verify wallet history or marketplace context. <br>
Mitigation: Provide complete transaction records, prior trades, wallet funding data, floor price context, and auction-house status before using its assessment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PaperBuddha/wash-trade-detector) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, JSON, guidance] <br>
**Output Format:** [Structured JSON assessment object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns wash-trade flag, confidence, matched pattern names, status, weight applied, exclusion flag, and analysis timestamp.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
