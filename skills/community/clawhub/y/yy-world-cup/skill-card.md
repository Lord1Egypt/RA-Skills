## Description: <br>
yyWorldCup helps agents predict World Cup match outcomes and generate China Sports Lottery strategy analysis using Elo factors, injury and weather signals, Polymarket calibration, and Beijing-time schedule handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deloyong](https://clawhub.ai/user/deloyong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze World Cup matches, compare model probabilities with market signals, and draft lottery strategy reports for review. Outputs are informational and should not be treated as betting advice. <br>

### Deployment Geography for Use: <br>
Global; includes China Sports Lottery context and Beijing Time handling. <br>

## Known Risks and Mitigations: <br>
Risk: The release includes maintenance code that can rewrite source files or create broad ZIP archives. <br>
Mitigation: Review the skill before installing and avoid auto_evolution modules, tune commands, or apply modes unless code modification and archive creation are intended. <br>
Risk: Normal prediction features require internet access and local caching. <br>
Mitigation: Run in an environment where outbound network access and cache locations are understood, and review cached data before relying on generated analysis. <br>
Risk: The skill produces lottery and market strategy analysis that could be mistaken for betting advice. <br>
Mitigation: Treat outputs as informational analysis for human review and keep the artifact's gambling-risk disclaimer visible in downstream use. <br>
Risk: The scanner guidance identifies an embedded API key and recommends removing or isolating risky maintenance functionality. <br>
Mitigation: Remove or rotate embedded credentials and separate auto-evolution, scheduler, and ZIP-generation code from the user-facing prediction workflow before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/deloyong/yy-world-cup) <br>
- [Publisher profile](https://clawhub.ai/user/deloyong) <br>
- [Comprehensive data model v3.1](docs/MODEL_v3.1.md) <br>
- [balldontlie FIFA World Cup API](https://api.balldontlie.io/fifa/worldcup/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown and plain-text analysis with Python examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include probability estimates, market comparisons, expected-value calculations, and strategy notes for human review.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
