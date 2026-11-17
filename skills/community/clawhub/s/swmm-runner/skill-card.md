## Description:

Run EPA SWMM (swmm5) simulations reproducibly and extract key metrics from the report file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhonghao1995](https://clawhub.ai/user/zhonghao1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after a SWMM model is assembled to run swmm5, produce a reproducible run directory, extract peak and continuity metrics, and compare report files for regression or GUI parity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe rptName or outName values can cause report or output files to be written outside the intended run directory.

Mitigation: Use trusted run parameters, avoid user-supplied report/output filenames, and keep run directories inside a disposable workspace until path validation is confirmed.

Risk: Untrusted SWMM input files may drive unexpected solver behavior or produce misleading simulation outputs.

Mitigation: Use only trusted .inp files and review generated reports, continuity errors, and manifest fields before relying on results.

## Reference(s):

- [Agentic SWMM project](https://github.com/Zhonghao1995/agentic-swmm-workflow)
- [ClawHub skill page](https://clawhub.ai/zhonghao1995/skills/swmm-runner)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands]

**Output Format:** [JSON manifests, SWMM report/output files, stdout/stderr text files, and parsed metric objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Run output may include rpt, out, stdout, stderr, manifest.json, peak metrics, continuity tables, and report comparison values.]

## Skill Version(s):

0.7.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
