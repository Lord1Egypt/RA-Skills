## Description: <br>
Filter relevant information from noise; extract claims, dedupe, rank impact, and preserve evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn large sets of messages, news, metrics, or notes into a decision-ready list of ranked signals with evidence and a separate noise bucket. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive private messages, secrets, or identifiers in the input dataset may be reflected in summaries or evidence pointers. <br>
Mitigation: Redact sensitive values before use and avoid feeding private message dumps unless those details are acceptable in the output. <br>
Risk: Broad activation could invoke the skill when a user only asks for a simple summary. <br>
Mitigation: Use it when ranking, deduplication, or evidence-preserving filtering is needed, and review the output before relying on it for decisions. <br>


## Reference(s): <br>
- [Signal vs Noise on ClawHub](https://clawhub.ai/mzfshark/signal-vs-noise) <br>
- [Publisher profile](https://clawhub.ai/user/mzfshark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, analysis] <br>
**Output Format:** [Markdown or structured text containing ranked_signals and discarded_noise sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each ranked signal should include a claim, why it matters, and at least one evidence pointer.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and skill.yml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
