## Description: <br>
SparkyFitness CLI for food diary, exercise tracking, biometric check-ins, and health summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronjanosch](https://clawhub.ai/user/aronjanosch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate the sparky CLI against a configured self-hosted SparkyFitness server for food, exercise, biometric, mood, summary, and trend workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps log privacy-sensitive food, exercise, weight, steps, and mood data to a configured SparkyFitness server. <br>
Mitigation: Use only a trusted server, protect the configured API key, and avoid entering health data that should not be stored on that server. <br>
Risk: Food and exercise search commands may fall back to external lookup providers. <br>
Mitigation: Prefer barcode, local IDs, or local library entries when privacy matters, and avoid sensitive search terms if external lookup fallback is a concern. <br>
Risk: Ambiguous search results can cause an agent to log the wrong food or exercise. <br>
Mitigation: Use barcode or UUID-based logging where possible, verify brand and macro details, and avoid relying on the first JSON result for ambiguous searches. <br>


## Reference(s): <br>
- [SparkyFitness](https://github.com/CodeWithCJ/SparkyFitness) <br>
- [sparky-cli](https://github.com/aronjanosch/sparky-cli) <br>
- [sparky-cli releases](https://github.com/aronjanosch/sparky-cli/releases) <br>
- [ClawHub skill page](https://clawhub.ai/aronjanosch/sparky) <br>
- [Publisher profile](https://clawhub.ai/user/aronjanosch) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and CLI usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-mode CLI examples for safer agentic use.] <br>

## Skill Version(s): <br>
0.3.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
