## Description:

Measure compositional structure in AI-generated images with the Visual Thinking Lens framework, flag default-mode patterns, and generate targeted re-prompts through configurable operators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rusparrish](https://clawhub.ai/user/rusparrish)

### License/Terms of Use:

Creative Commons Attribution 4.0 International (CC BY 4.0)

## Use Case:

Developers, creators, and image-generation users use this skill to diagnose generated-image composition, report VTL coordinates, and produce rule-based re-prompt suggestions when default-mode patterns are detected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes image files or folders selected by the user and can create or overwrite metrics.jsonl or prompts.json outputs.

Mitigation: Run it only on intended local paths, choose explicit output locations for prompt generation, and review existing output files before batch analysis.

Risk: Python dependencies are declared as package names without pinned versions.

Mitigation: Pin and review dependency versions before production use.

Risk: Custom operator trigger expressions are evaluated by the regeneration script.

Mitigation: Review changes to operators.yaml before use and keep trigger logic limited to the supported numeric expressions.

Risk: Low-confidence or failed measurements can produce misleading composition guidance if the gate is ignored.

Mitigation: Honor the valid and mask_status fields: stop on FAIL and treat WARN results as indicative rather than definitive.

## Reference(s):

- [VTL Metric Reference](references/vtl-metrics.md)
- [Visual Thinking Lens framework](https://github.com/rusparrish/Visual-Thinking-Lens)
- [Russell Parrish](https://artistinfluencer.com)
- [ClawHub skill page](https://clawhub.ai/rusparrish/skills/vtl-image-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON metrics or prompt-variant outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill analyzes local image files or folders, reports PASS/WARN/FAIL measurement status, and may write metrics.jsonl or prompts.json outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
