## Description: <br>
Refines existing SOPs by removing redundant steps, adding exception paths, rollback guidance, and quality gates without changing approval boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations teams, process owners, and employees use this skill to turn existing SOP text and pain-point feedback into reviewable Markdown recommendations for cleaner, safer, and more complete procedures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundle has low provenance and includes a local Python script. <br>
Mitigation: Install only if comfortable running the script, inspect the artifact before use, and run it only on specific SOP files you intend to process. <br>
Risk: SOP inputs may contain sensitive operational, customer, or employee information. <br>
Mitigation: Redact sensitive material where possible and avoid broad directory scans over unrelated or confidential files. <br>
Risk: Generated SOP changes could be incomplete or unsuitable for the organization. <br>
Mitigation: Treat outputs as review drafts, preserve existing approval boundaries, and verify rollback, exception, and quality-gate changes with the responsible owners. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/sop-refiner) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [README](artifact/README.md) <br>
- [Specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>
- [Smoke test](artifact/tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown by default, with optional JSON output from the bundled script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewable SOP recommendations and checklists; generated content should be reviewed before operational use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
