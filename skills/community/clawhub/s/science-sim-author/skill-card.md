## Description: <br>
Generates self-contained interactive science simulations as a single offline index.html from a SimSpec YAML or JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dimgouso](https://clawhub.ai/user/dimgouso) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Educators, curriculum developers, and agents use this skill to turn STEM SimSpec YAML or JSON into offline browser simulations with controls, plots, and inquiry worksheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated simulations intentionally include runnable browser JavaScript. <br>
Mitigation: Review generated index.html before opening or sharing it, especially when the SimSpec came from someone else. <br>
Risk: Generated HTML could become unsafe if external scripts, network calls, telemetry, secrets, or unexpected browser permissions are added. <br>
Mitigation: Confirm the file remains self-contained and contains no external scripts, runtime network access, telemetry, secrets, or unexpected browser permissions. <br>
Risk: A malformed or unclear SimSpec can produce misleading educational behavior or incorrect model equations. <br>
Mitigation: Validate the SimSpec against the bundled schema and review the generated equations, plots, readouts, and worksheet before classroom use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dimgouso/science-sim-author) <br>
- [SimSpec schema](artifact/templates/sim_spec_schema.json) <br>
- [Single-file HTML template](artifact/templates/sim_single_file_html_template.html) <br>
- [Validation checklist](artifact/rubrics/validation_checklist.md) <br>
- [Security notes](artifact/rubrics/security_notes.md) <br>
- [Pedagogy inquiry prompts](artifact/rubrics/pedagogy_inquiry_prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, text, guidance] <br>
**Output Format:** [Single self-contained HTML file with inline CSS and JavaScript] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external runtime dependencies; output is intended to run offline in a browser.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
