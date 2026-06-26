## Description: <br>
Automated abstract screening tool for systematic literature reviews with PRISMA workflow support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and evidence-review teams use this skill to screen academic abstracts against configurable inclusion and exclusion criteria, produce reviewable decision rationales, and prepare PRISMA-style screening outputs. Human reviewers remain responsible for final inclusion and exclusion decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screening recommendations can be incorrect or incomplete if criteria, thresholds, language assumptions, or abstract content do not match the review protocol. <br>
Mitigation: Customize and review the YAML criteria before use, inspect conflicts and low-confidence records, and require human verification before reporting final inclusion decisions. <br>
Risk: The packaged Python script reads local reference files and writes screening outputs to the workspace. <br>
Mitigation: Run it only on intended input files in a controlled workspace and review generated CSV and JSON outputs before sharing. <br>
Risk: Dependency declarations require verification before real use. <br>
Mitigation: Confirm the Python environment and dependencies before execution, then run the documented compile and help checks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aipoch-ai/systematic-review-screener) <br>
- [criteria_template.yaml](references/criteria_template.yaml) <br>
- [sample_references.csv](references/sample_references.csv) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; the packaged script can generate CSV and JSON screening outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces included, excluded, conflict, PRISMA, and screening-log artifacts when run with valid reference and criteria files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
