## Description: <br>
SparkyFitness CLI for food diary, exercise tracking, biometric check-ins, and health summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronjanosch](https://clawhub.ai/user/aronjanosch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent compose and run sparky CLI workflows against a configured self-hosted SparkyFitness server for food, exercise, check-in, diary, summary, and trend tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health records and the SparkyFitness API key are sensitive. <br>
Mitigation: Use HTTPS, keep the API key out of shared terminals and logs, and prefer a revocable key when available. <br>
Risk: An agent may log, delete, or remove the wrong food, exercise, or health record. <br>
Mitigation: Have the agent confirm exact entries, brands, IDs, quantities, and dates before changing health records. <br>
Risk: The skill relies on an external CLI and a configured self-hosted server. <br>
Mitigation: Install only if you trust the sparky CLI and the configured SparkyFitness server. <br>


## Reference(s): <br>
- [ClawHub SparkyFitness Skill](https://clawhub.ai/aronjanosch/sparkyfitness) <br>
- [SparkyFitness Project](https://github.com/CodeWithCJ/SparkyFitness) <br>
- [sparky CLI Source](https://github.com/aronjanosch/sparky-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON-oriented CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill depends on an installed sparky binary and a configured SparkyFitness server URL and API key.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
