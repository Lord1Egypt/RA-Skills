## Description: <br>
Checks whether conclusions in research or analysis are supported by provided evidence and highlights gaps in the evidence chain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, reviewers, and developers use this skill to review research drafts, claims, and evidence summaries for support, gaps, missing evidence, suggested revisions, and confidence judgments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-provided research material and can write a report file, so sensitive input or an unsafe output path could expose or overwrite local content. <br>
Mitigation: Use dry-run or stdout for sensitive reviews, provide only intended input files, and avoid writing output to important paths. <br>
Risk: The output is an evidence-checking aid and may miss context or produce incomplete confidence judgments. <br>
Mitigation: Treat results as review guidance, not peer review or final factual validation, and verify claims against authoritative sources before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/research-claim-checker) <br>
- [README](artifact/README.md) <br>
- [Output template](artifact/resources/template.md) <br>
- [Structured output spec](artifact/resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured Markdown report, with optional JSON output from the local helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a report to a user-specified output path or emit to stdout; dry-run mode is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
