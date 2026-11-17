## Description:

Batch pre-filing tax self-check that runs 14 tax checks for each entity folder and reports one conclusion line per entity, with findings citing source files and line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Tax accountants and bookkeeping teams use this skill before filing to batch-check customer or entity tax materials for arithmetic and reconciliation issues. It supports local review of VAT input deduction, surtaxes, stamp duty, R&D expense collection, export rebate documents, corporate income tax checks, deferred tax, property and land-use tax, land appreciation tax, and environmental tax materials.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill reads tax-material files from the input path supplied by the user.

Mitigation: Run it only against the intended local materials directory and keep unrelated sensitive files outside that path.

Risk: Outputs may be mistaken for tax filing advice or complete compliance assurance.

Mitigation: Use the results as arithmetic and reconciliation assistance, then have a qualified reviewer assess tax treatment, policy currency, and filing decisions.

Risk: Missing materials or unrecognized table headers can leave checks unexecuted.

Mitigation: Review the not-run sub-check lists and any material-insufficient messages before relying on a clean-looking result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/tax-filing-pack-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Human-readable stdout report, or JSON when --json is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite object names plus source files and line numbers; results are produced locally and are not written to files.]

## Skill Version(s):

1.0.34 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
