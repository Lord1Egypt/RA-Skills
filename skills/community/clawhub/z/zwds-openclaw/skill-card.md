## Description: <br>
Generates structured Zi Wei Dou Shu chart JSON through a local Node CLI and guides agents to interpret only the generated JSON, with documented true-solar-time and location rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luyao-inc](https://clawhub.ai/user/luyao-inc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate Zi Wei Dou Shu charts from birth time, gender, and optional birthplace or longitude, then produce evidence-bound astrology readings from the returned JSON. Developers can also use the bundled Node CLI examples and fixtures to test repeatable chart generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birth time, birthplace, gender, longitude, and fixture files can expose private personal details. <br>
Mitigation: Keep personal fixture JSON files out of shared repositories, delete them when no longer needed, and treat chart inputs and outputs as private. <br>
Risk: The CLI can fall back to a default longitude when a birthplace is missing or not found, which can affect time and chart interpretation. <br>
Mitigation: Review meta warnings and ask for an explicit decimal longitude when the birthplace is ambiguous or outside the bundled location table. <br>
Risk: The true-solar-time model is simplified and may differ from other Zi Wei Dou Shu conventions. <br>
Mitigation: State the skill's timing assumptions when precision matters, especially around boundary times or when users compare against another school. <br>
Risk: Regenerating longitude data intentionally performs network requests. <br>
Mitigation: Run the longitude regeneration script only when refreshing bundled location data is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luyao-inc/zwds-openclaw) <br>
- [iztro quick start](https://iztro.com/quick-start.html) <br>
- [modood Administrative-divisions-of-China](https://github.com/modood/Administrative-divisions-of-China) <br>
- [artifact/reference.md](artifact/reference.md) <br>
- [artifact/examples.md](artifact/examples.md) <br>
- [artifact/zwds-cli/README.md](artifact/zwds-cli/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON from the CLI and Markdown or text guidance for chart interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create fixture JSON files for repeated readings; interpretations should remain grounded in the generated data and meta warnings.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
