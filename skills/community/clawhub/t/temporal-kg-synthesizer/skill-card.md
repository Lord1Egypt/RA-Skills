## Description: <br>
Actively parses daily session logs and unstructured memory files to extract entities, temporal data, and relationships into a structured Knowledge Graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ElMoorish](https://clawhub.ai/user/ElMoorish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to parse daily memory logs into persistent entity Markdown files, then consult those files when answering entity or timeline questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private OpenClaw memory logs may be parsed into persistent entity files containing sensitive names, projects, or relationships. <br>
Mitigation: Install only where that persistence is acceptable and review ~/.openclaw/workspace/memory/entities/ after use. <br>
Risk: The bundled cron setup can enable daily background processing of workspace memory. <br>
Mitigation: Avoid running cron_setup.sh unless daily background processing is intended and approved for the workspace. <br>
Risk: Generated entity files may be incomplete or imprecise because extraction depends on spaCy or a regex fallback. <br>
Mitigation: Treat generated entity and timeline material as an aid for review, not as an authoritative record. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ElMoorish/temporal-kg-synthesizer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown status output plus generated Markdown entity files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes entity Markdown files under ~/.openclaw/workspace/memory/entities/ when dated memory logs are present.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
