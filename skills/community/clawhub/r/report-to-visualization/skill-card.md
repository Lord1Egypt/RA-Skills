## Description: <br>
Converts Chinese-language text reports into strict MODULE-format visualization component JSON when users ask for report visualization, chart-based presentation, or richer visual reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and report-writing agents use this skill to transform Chinese-language report content into structured visualization modules for charts, cards, timelines, alerts, and comparison lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated visualization JSON can be inaccurate, incomplete, or mismatched to the report language or strict component schema. <br>
Mitigation: Review generated JSON for accuracy, completeness, language fit, and schema compliance before using it in a report workflow. <br>
Risk: The skill may activate on broad report or chart wording and produce a visualization response when the user expected a different kind of analysis. <br>
Mitigation: Confirm that the user wants a seller-report visualization component output before relying on the generated configuration. <br>


## Reference(s): <br>
- [Anti-patterns Reference](references/anti-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, configuration] <br>
**Output Format:** [A seller-report fenced Markdown code block containing a single JSON object with modules and visualization component configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output must contain no prose outside the seller-report code block.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
