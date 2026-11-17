## Description:

Generate self-contained interactive science simulations as a single index.html from a SimSpec YAML or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimgouso](https://clawhub.ai/user/dimgouso)

### License/Terms of Use:


## Use Case:

Educators, curriculum authors, and developers use this skill to turn validated SimSpec YAML or JSON into offline classroom simulations with parameter sliders, plots, local exports, and inquiry worksheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted SimSpec text may be embedded into generated HTML in a way that can run unintended JavaScript.

Mitigation: Use trusted SimSpecs only, or fix the template to safely encode JSON for inline script contexts before accepting third-party or student-supplied specs.

Risk: Generated simulations can contain inaccurate equations, parameters, or learning prompts if the input SimSpec is wrong or incomplete.

Mitigation: Validate each SimSpec against the bundled schema and review the generated model equations, readouts, plots, and worksheet against the validation checklist before classroom or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dimgouso/skills/science-sim-author)
- [Publisher profile](https://clawhub.ai/user/dimgouso)
- [SimSpec schema](artifact/templates/sim_spec_schema.json)
- [Single-file HTML template](artifact/templates/sim_single_file_html_template.html)
- [Validation checklist](artifact/rubrics/validation_checklist.md)
- [Security notes](artifact/rubrics/security_notes.md)

## Skill Output:

**Output Type(s):** [code, configuration, guidance]

**Output Format:** [A single self-contained index.html file with inline HTML, CSS, and JavaScript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs offline in a browser, uses local JSON and CSV export, and does not require external assets, package managers, or runtime network access.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
