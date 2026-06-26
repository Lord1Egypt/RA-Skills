## Description: <br>
Analyzes retail performance across target attainment, month-over-month movement, historical baseline, and benchmark dimensions to explain performance below expectations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwyang7](https://clawhub.ai/user/gwyang7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail operators and analysts use this skill to generate a concise performance evaluation report for a store, comparing actual performance against goals, recent periods, historical baselines, and peer benchmarks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can present hardcoded mock retail performance numbers as real analysis. <br>
Mitigation: Review the output before using it for business decisions and require real, clearly sourced data before deployment. <br>
Risk: The artifact advertises Benchmark analysis, but the provided implementation does not implement the advertised Benchmark dimension. <br>
Mitigation: Confirm Benchmark analysis is implemented and tested before relying on benchmark-based conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gwyang7/retail-performance-evaluation-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/gwyang7) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown report text and Python dictionary results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include status, current and expected values, achievement rates, findings, and recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
