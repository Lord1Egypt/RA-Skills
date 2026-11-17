## Description:

SMILES De-salter batch-processes chemical SMILES strings to remove salt or counterion components and retain the active core.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data scientists, and cheminformatics teams use this skill to desalt CSV, TSV, SMI, or single SMILES inputs and produce reviewable desalted SMILES outputs with status information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency hygiene requires review because the tool depends on pandas and RDKit without pinned versions.

Mitigation: Install in a project workspace or virtual environment, pin and review pandas and RDKit versions, and run the documented py_compile smoke check before production use.

Risk: The utility reads user-provided input files and writes output files in the local workspace.

Mitigation: Use explicit input and output paths for SMILES de-salting tasks, verify paths before execution, and review generated files before sharing or downstream use.

Risk: The de-salting heuristic keeps the largest component, which may require review for co-crystals or multi-component drugs.

Mitigation: Sample and verify results for chemically sensitive datasets, especially when multiple active components may be present.

## Reference(s):

- [Runtime Checklist](references/runtime_checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and CSV, TSV, SMI, or text outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces desalted_smiles and status fields for batch file processing; single-SMILES mode prints input, output, and status.]

## Skill Version(s):

1.0.0 (source: server release evidence and script metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
