## Description:

Deterministic rainfall/climate formatting for SWMM that converts timestamped rainfall CSV files into SWMM-ready [TIMESERIES] lines and [RAINGAGES] helper snippets for swmm-builder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhonghao1995](https://clawhub.ai/user/zhonghao1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and stormwater engineers use this skill to prepare measured or synthetic rainfall data for SWMM workflows, producing deterministic timeseries text, raingage snippets, and audit JSON for model assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed or untrusted station IDs, gage IDs, or series-name templates can corrupt or alter generated SWMM configuration fragments.

Mitigation: Validate identifiers to simple SWMM-safe names and review generated [TIMESERIES] and [RAINGAGES] outputs before adding them to a model.

Risk: Untrusted CSV or DAT rainfall inputs can produce misleading model inputs even when conversion is deterministic.

Mitigation: Use trusted rainfall sources where possible, validate input units and time windows, and compare the generated JSON summary against the source data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhonghao1995/skills/swmm-climate)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Markdown guidance with command examples; generated SWMM text and JSON files when scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local file outputs; no hidden network, credential, or persistence behavior reported by security evidence]

## Skill Version(s):

0.7.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
