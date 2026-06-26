## Description: <br>
Detects and rewrites English text to remove AI-writing signals through calibration, artifact removal, vocabulary cleanup, content deflation, structural reconstruction, and texture injection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[idcesares](https://clawhub.ai/user/idcesares) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and writing-focused agents use this skill to review English drafts for AI-writing signs and produce rewritten text that preserves meaning, register, and author constraints. It is intended for English text only, with limited structural flagging rather than full rewriting for non-English input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be misused to hide AI authorship or bypass disclosure, academic integrity, workplace, or publication rules. <br>
Mitigation: Use it only where rewriting is allowed, preserve required disclosure, and review outputs against the applicable policy before use. <br>
Risk: Aggressive rewriting can change meaning, register, or factual claims in the source text. <br>
Mitigation: Follow the calibration step, preserve the source voice and constraints, and compare the rewrite with the original before publishing. <br>
Risk: The full workflow is calibrated for English and may produce unreliable vocabulary or statistical judgments for other languages. <br>
Mitigation: Decline full non-English rewrites or limit the response to structural pattern flagging with an explicit caveat. <br>


## Reference(s): <br>
- [Anti-patterns - humanization gone wrong](artifact/references/anti-patterns.md) <br>
- [Genre playbooks - calibrating the rewrite to context](artifact/references/genre-playbooks.md) <br>
- [Statistical guide - measuring and improving text humanness](artifact/references/statistical-guide.md) <br>
- [Structural patterns - deep reference](artifact/references/structural-patterns.md) <br>
- [AI vocabulary by era - full lexicon](artifact/references/vocabulary-by-era.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text, depending on requested rewrite mode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Express mode returns only the rewrite; standard and heavy modes can include change summaries, confidence notes, and optional scoring when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
