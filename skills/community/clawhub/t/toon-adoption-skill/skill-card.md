## Description: <br>
Optimize token usage by adopting the compact TOON format for data storage and context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nelohenriq](https://clawhub.ai/user/nelohenriq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to parse, generate, and store structured data in TOON so long-running notes, logs, configurations, and session summaries consume fewer LLM context tokens than equivalent JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or updating through ClawHub registry tooling can modify local skill folders and may store a local API token for authenticated operations. <br>
Mitigation: Review the CLI documentation and install only from the intended release; use appropriate local token handling and permissions. <br>
Risk: Incorrect TOON formatting can make structured data ambiguous or harder for an agent to parse. <br>
Mitigation: Keep 2-space indentation strict, declare array lengths, quote values that contain commas or significant whitespace, and validate important conversions against JSON. <br>


## Reference(s): <br>
- [ClawHub TOON Release](https://clawhub.ai/nelohenriq/toon-adoption-skill) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with TOON code blocks and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Encourages UTF-8 .toon files, strict 2-space indentation, explicit array lengths, and tabular arrays for uniform object lists.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
