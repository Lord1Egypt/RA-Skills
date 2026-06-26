## Description: <br>
Analyze ChatGPT conversation exports to discover cognitive archetypes and optimize AI-human communication patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebastianffx](https://clawhub.ai/user/sebastianffx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to analyze local ChatGPT exports, generate cognitive profile files, and adapt agent instructions to their observed communication patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ChatGPT exports and generated cognitive profiles can contain sensitive personal or work information. <br>
Mitigation: Run analysis locally, keep exports and profiles out of shared repositories, and redact or sample data where possible. <br>
Risk: Profile text copied into agent instruction files can expose personal communication patterns or misleading recommendations. <br>
Mitigation: Review generated profile content before adding it to SOUL.md, AGENTS.md, or other shared agent configuration. <br>
Risk: The WildChat test script fetches an external dataset when intentionally executed. <br>
Mitigation: Do not run test_wildchat.py unless external dataset access is intended; use a virtual environment and pin dependencies for reproducibility. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/sebastianffx/user-cognitive-profiles) <br>
- [Methodology](references/methodology.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON profile files, Markdown prompt snippets, console summaries, and optional Markdown comparison reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are local files derived from user-provided conversation exports and should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
