## Description: <br>
Mine unstructured clinical text from MIMIC-IV to extract diagnostic logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and clinical data analysts use this skill to convert authorized MIMIC-IV clinical note text into structured entities, relationships, timelines, and diagnostic or treatment logic for reviewable analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save sensitive patient-level clinical extracts to disk. <br>
Mitigation: Use only authorized, preferably de-identified or synthetic clinical text; pass an explicit secure output path and restrict access to generated files. <br>
Risk: Processing real clinical notes can expose regulated health information if run in an uncontrolled environment. <br>
Mitigation: Run the tool in a controlled local environment with appropriate data-handling approval before using real datasets. <br>
Risk: Unpinned NLP and data-processing dependencies can change behavior across runs. <br>
Mitigation: Pin or lock dependencies before using the skill on real datasets. <br>


## Reference(s): <br>
- [MIMIC-IV Clinical Database](https://physionet.org/content/mimiciv/) <br>
- [scispaCy](https://allenai.github.io/scispacy/) <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/unstructured-medical-text-miner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and CLI examples, plus structured JSON, FHIR-compatible, knowledge graph, or temporal event outputs from the packaged miner.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write structured output files to an explicit path; raw clinical text should remain excluded unless intentionally configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
