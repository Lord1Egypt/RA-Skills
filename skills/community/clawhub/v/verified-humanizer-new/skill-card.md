## Description: <br>
Transform AI-generated content into natural, human-sounding writing, measure the improvement, and optionally verify the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ch4812](https://clawhub.ai/user/ch4812) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and agents use this skill to rewrite AI-assisted drafts into clearer, less formulaic text while preserving meaning and producing a local before/after evaluation. Optional verification should use only structured metrics, not original or rewritten text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package identity or version mismatch could weaken provenance confidence. <br>
Mitigation: Confirm the ClawHub skill identity, publisher handle, slug, and version before relying on provenance for higher-trust workflows. <br>
Risk: Optional verification could expose private text if used incorrectly. <br>
Mitigation: Send only structured evaluation metrics to verification and keep original and rewritten text local. <br>
Risk: A rewritten draft could change meaning or introduce unsupported facts. <br>
Mitigation: Review the output against the original intent and use the rewrite checklist before returning or publishing the text. <br>


## Reference(s): <br>
- [Verified Humanizer examples](references/examples.md) <br>
- [OpenClaw integration notes](references/openclaw-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON object with rewritten text, change notes, evaluation metrics, and optional verification fields; Markdown reports may also be produced.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rewriting and evaluation are local by default; optional verification is limited to structured metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
